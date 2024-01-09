import json
import luigi
import pandas as pd
import numpy as np
from time import sleep
from bs4 import BeautifulSoup

from luigi.cmdline import luigi_run
from datetime import datetime, time, timedelta

from tasks.base import CsvFileOutput, FtpUploadedOutput, Runner
from luigi.util import requires

from tcomextetl.common.csv import dict_to_row, save_csvrows
from tcomextetl.common.utils import rewrite_file
from tcomextetl.extract.tvplus_requests import TvPlusParser, TvPlusProgramsParser
from tcomextetl.common.dates import DEFAULT_DATETIME_FORMAT_WITHT, today

start_host = 'https://kt.server-api.lfstrm.tv'
programs_host = 'https://tv.telecom.kz/channels'

tv_categories = {'detectives': 'L3R2L2dlbnJlcy9kZXRlY3RpdmU=',
                 'newest': 'L3R2L2ZlYXR1cmVk',
                 'drama': 'L3R2L2dlbnJlcy9kcmFtYQ==',
                 'thriller': 'L3R2L2dlbnJlcy90aHJpbGxlcg==',
                 'historical': 'L3R2L2dlbnJlcy9oaXN0b3J5',
                 'Семейные': 'L3R2L2dlbnJlcy9mYW1pbHk=',
                 'Военные ': 'L3R2L2dlbnJlcy93YXI=',
                 # 'Ток-шоу ': 'L3R2L2dlbnJlcy90YWxrc2hvdw==',
                 # 'Спорт ': 'L3R2L2dlbnJlcy9zcG9ydA==',
                 'Комедии ': 'L3R2L2dlbnJlcy9jb21lZHk=',
                 'Боевики ': 'L3R2L2dlbnJlcy9hY3Rpb24=',
                 'Документальные ': 'L3R2L2dlbnJlcy9kb2N1bWVudGFs',
                 'Мелодрама ': 'L3R2L2dlbnJlcy9tZWxvZHJhbWE=',
                 'Мультфильмы ': 'L3R2L2dlbnJlcy9jYXJ0b29u'}


class TvPlusProgramsOutput(CsvFileOutput):

    from_to = luigi.TupleParameter(default=())
    timeout = luigi.FloatParameter(default=10.0)


    @property
    def programs_params(self):
        params = dict()
        params['dateFrom'], params['dateTo'] = self.from_to
        return params

    def run(self):

        headers = dict()
        headers['accept'] = 'application/json'

        programs_url = f'{programs_host}/list'

        parser = TvPlusProgramsParser(
            programs_url,
            headers=headers
        )
        parser_text = parser.load()

        soup = BeautifulSoup(parser_text, "html.parser")
        script = soup.findAll('script')
        data = str(script[3])
        start_index = data.find('{')
        end_index = data.rfind('}', 0, -30)
        text_for_json = data[start_index:end_index + 1]

        json_data = json.loads(text_for_json)
        programs_df = pd.DataFrame(json_data['tvChannels']['list']).T.reset_index().drop(columns=['index'])
        date_from = self.programs_params['dateFrom']
        date_to = self.programs_params['dateTo']
        date_from_format = datetime.strptime(date_from, DEFAULT_DATETIME_FORMAT_WITHT)
        date_to_format = datetime.strptime(date_to, DEFAULT_DATETIME_FORMAT_WITHT)
        timestamp_from = int(datetime.combine(date_from_format, time.min).timestamp())
        timestamp_to = int(datetime.combine(date_to_format, time.max).timestamp())
        channels = pd.DataFrame(
            columns=['channel_id', 'channel', 'channel_description', 'channel_genres', 'channel_age_rating',
                     'channel_start_time', 'channel_stop_time'])
        for i in range(len(programs_df)):

            temp = programs_df.iloc[i]['info']
            info = []

            if temp['EPGBounds']['min'] < 0:
                min_time = str(date_to)
            else:
                min_time = str(datetime.fromtimestamp(temp['EPGBounds']['min']))
            if temp['EPGBounds']['max'] < 0:
                max_time = str(date_to)
            else:
                max_time = str(datetime.fromtimestamp(temp['EPGBounds']['max']))
            info.append([programs_df.iloc[i]['id'],
                         temp['metaInfo']['title'],
                         temp['metaInfo']['description'],
                         temp['metaInfo']['genres'],
                         temp['metaInfo']['age_rating'],
                         min_time,
                         max_time])
            channels = pd.concat([channels,
                                  pd.DataFrame(info, columns=['channel_id', 'channel', 'channel_description',
                                                              'channel_genres', 'channel_age_rating',
                                                              'channel_start_time', 'channel_stop_time'])])

        for j in channels['channel_id']:
            stp = False
            for t in range(5):
                try:
                    programs_url = f"{start_host}/channels/{j}/programs?period={timestamp_from}:{timestamp_to}"
                    programs_parser = TvPlusParser(
                        programs_url
                    )

                    break
                except:
                    sleep(self.timeout)
                    if t == 4:
                        stp = True
            if stp:
                break

            dataframe = programs_parser.load()
            rows_count = 0

            try:
                for i in range(len(dataframe['programs'])):
                    if datetime.fromtimestamp(dataframe['programs'][i]['scheduleInfo']['start']) > date_to_format:
                        continue
                    info = []
                    if dataframe['programs'][i]['scheduleInfo']['start'] < 0:
                        min_time = np.nan
                    else:
                        min_time = str(datetime.fromtimestamp(dataframe['programs'][i]['scheduleInfo']['start']))
                    if dataframe['programs'][i]['scheduleInfo']['end'] < 0:
                        max_time = np.nan
                    else:
                        max_time = str(datetime.fromtimestamp(dataframe['programs'][i]['scheduleInfo']['end']))
                    if dataframe['programs'][i]['updateInfo']['mtime'] < 0:
                        upd = np.nan
                    else:
                        upd = str(datetime.fromtimestamp(dataframe['programs'][i]['updateInfo']['mtime']))
                    channel_row = {'channel_id': dataframe['id'],
                                   'channel': channels[channels['channel_id']==j]['channel'].values[0],
                                   'program_id': dataframe['programs'][i]['id'],
                                   'program': dataframe['programs'][i]['metaInfo']['title'],
                                   'description': dataframe['programs'][i]['metaInfo']['description'],
                                   'ageRating': dataframe['programs'][i]['metaInfo']['age_rating'],
                                   'start': min_time,
                                   'end': max_time,
                                   'duration': dataframe['programs'][i]['scheduleInfo']['duration'] / 60,
                                   'update_info': upd}
                    data = dict_to_row(channel_row, self.struct)
                    save_csvrows(self.output_fpath, [data], delimiter=';')
                    rows_count += 1

            except:
                channel_row = {'channel_id': dataframe['id'],
                               'channel': channels[channels['channel_id'] == j]['channel'].values[0],
                               'program_id': np.nan,
                               'program': np.nan,
                               'description': np.nan,
                               'ageRating': np.nan,
                               'start': np.nan,
                               'end': np.nan,
                               'duration': np.nan,
                               'update_info': np.nan}
                data = dict_to_row(channel_row, self.struct)
                save_csvrows(self.output_fpath, [data], delimiter=';')
                rows_count += 1

        stat = parser.stat
        stat.update({'parsed': rows_count})
        rewrite_file(self.success_fpath, json.dumps(stat))
        sleep(self.timeout)


@requires(TvPlusProgramsOutput)
class TvPlusProgramsOutputFtpOutput(FtpUploadedOutput):
    pass


class TvPlusProgramsRunner(Runner):

    name = luigi.Parameter()
    start_date = luigi.DateParameter(default=today() - timedelta(days=1))
    end_date = luigi.DateParameter(default=today())
    timeout = luigi.IntParameter(default=2)

    @property
    def params(self):
        params = super(TvPlusProgramsRunner, self).params
        # noinspection PyTypeChecker
        s_date = datetime.combine(self.start_date, datetime.min.time()).isoformat()
        e_date = datetime.combine(self.end_date, datetime.min.time()).isoformat()
        params['from_to'] = (
            s_date,
            e_date
        )
        return params

    def requires(self):
        return TvPlusProgramsOutputFtpOutput(**self.params)


class TvPlusProgramsCheckList(TvPlusProgramsRunner):
    name = luigi.Parameter('tvplus_programs')


class TvPlusCinemaOutput(CsvFileOutput):

    endpoint = luigi.Parameter()

    @staticmethod
    def movies_params(category_id, limit=1000):
        params = {"categoryId": category_id, "limit": limit}
        return params

    def run(self):

        api_url = start_host + '/' + str(self.endpoint)

        parser = TvPlusParser(
            api_url
        )

        movies_ids = {}
        for category_id in tv_categories.values():
            category_info = parser.load(self.movies_params(category_id))
            for movie_id in category_info['titles']:
                movies_ids[movie_id['id']] = movie_id['title']

        rows_count = 0

        for movie_id in movies_ids.keys():
            try:
                parser_movie = TvPlusParser(
                    f'{api_url}/{movie_id}'
                )
                movie = parser_movie.load()
                preview = movie['preview']
                detail = movie['details']
                if not preview['hasSeries']:
                    movie_details = detail['mediaItems'][0]['playbackMethods'][0]['params'][2]['value']
                    movie_row = {'id': movie_details,
                                 'title': preview['title'],
                                 'genre': preview['categories'][0]['title'],
                                 'category': 'Movie',
                                 'ageRating': preview['ageRating'],
                                 'ratingImdb': preview['ratingImdb'],
                                 'ratingKp': preview['ratingKp'],
                                 'description': detail['description']}
                    data = dict_to_row(movie_row, self.struct)
                    save_csvrows(self.output_fpath, [data], delimiter=';')
                    rows_count += 1
                else:
                    for i in detail['seasons']:
                        parser_series = TvPlusParser(
                            f'{api_url}/{i["id"]}'
                        )
                        series_info = parser_series.load()
                        series_details = series_info['details']['mediaItems'][0]['playbackMethods'][0]['params'][2][
                            'value']
                        series_row = {'id': series_details,
                                      'title': preview['title'],
                                      'genre': preview['categories'][0]['title'],
                                      'category': 'Series',
                                      'ageRating': preview['ageRating'],
                                      'ratingImdb': preview['ratingImdb'],
                                      'ratingKp': preview['ratingKp'],
                                      'description': detail['description']}
                        data = dict_to_row(series_row, self.struct)
                        save_csvrows(self.output_fpath, [data], delimiter=';')
                        rows_count += 1

            except:
                time.sleep(1)

        stat = parser.stat
        stat.update({'parsed': rows_count})
        rewrite_file(self.success_fpath, json.dumps(stat))


@requires(TvPlusCinemaOutput)
class TvPlusCinemaOutputFtpOutput(FtpUploadedOutput):
    pass


class TvPlusCinemaRunner(Runner):

    @property
    def params(self):
        params = super(TvPlusCinemaRunner, self).params

        return params

    def requires(self):
        return TvPlusCinemaOutputFtpOutput(**self.params)


class TvPlusCinemaStartCheckList(TvPlusCinemaRunner):
    name = luigi.Parameter('tvplus_cinema_start')


class TvPlusCinemaKazvodCheckList(TvPlusCinemaRunner):
    name = luigi.Parameter('tvplus_cinema_kazvod')


if __name__ == '__main__':
    luigi_run()
