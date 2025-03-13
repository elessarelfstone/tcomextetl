from settings import ROCKETDATA_TOKEN
import luigi
from luigi.parameter import ParameterVisibility
from luigi.util import requires
from tasks.base import ApiToCsv, FtpUploadedOutput, Runner
from tcomextetl.common.csv import save_csvrows, dict_to_row

from tcomextetl.common.utils import rewrite_file
import json

from tcomextetl.extract.rocket_requests import RocketDataParser

rocketdata_url = "https://api.rocketdata.io/public/v4"

class RocketDataReviewsOutput(ApiToCsv):
    endpoint = luigi.Parameter(default="/reviews/")
    token = luigi.Parameter(visibility=ParameterVisibility.HIDDEN)
    from_to = luigi.TupleParameter(default=())
    timeout = luigi.IntParameter(default=10)

    @property
    def url(self):
        return f'{rocketdata_url}{self.endpoint}'

    @property
    def headers(self):
        return {'Authorization': f'Token {self.token}'}

    @property
    def request_params(self):
        return {}

    def run(self):
        dates = self.from_to
        parser = RocketDataParser(self.url, dates, headers=self.headers,
                                  timeout=self.timeout)
        parser.set_parsed_count(self.stat.get('parsed', 0))

        for data in parser:
            # Save each batch of reviews into CSV rows.
            save_csvrows(self.output_fpath,
                         [dict_to_row(d, self.struct) for d in data],
                         quotechar='"')
            self.set_status_info(*parser.status_percent)
            stat = parser.stat
            stat.update(self.request_params)
            rewrite_file(self.stat_fpath, json.dumps(stat))

        self.finalize()


@requires(RocketDataReviewsOutput)
class RocketDataReviewsFtpOutput(FtpUploadedOutput):
    pass


class RocketDataRunner(Runner):
    start_date = luigi.Parameter(default=Runner.yesterday())
    end_date = luigi.Parameter(default=Runner.yesterday())

    token = luigi.Parameter(visibility=ParameterVisibility.HIDDEN)

    def requires(self):
        params = self.params
        if not self.all_data:
            params['from_to'] = (self.start_date, self.end_date)
        return RocketDataReviewsFtpOutput(token=self.token, **params)


class RocketDataReviews(RocketDataRunner):
    name = luigi.Parameter('rocketdata_reviews')
    token = luigi.Parameter(default=ROCKETDATA_TOKEN, visibility=ParameterVisibility.HIDDEN)


if __name__ == '__main__':
    luigi.run()
