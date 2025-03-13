from datetime import datetime, timedelta
from collections import deque
import time
from requests.exceptions import ReadTimeout, ConnectTimeout

from tcomextetl.common.dates import dates_between
from tcomextetl.extract.api_requests import ApiRequests

class RocketDataParser(ApiRequests):
    """
    Parser for RocketData API that iterates over a range of dates.
    """
    def __init__(self, url, dates, headers, **kwargs):
        super(RocketDataParser, self).__init__(**kwargs)
        self.url = url
        self.headers = headers
        # Create a deque of dates between start_date and end_date.
        self._dates = deque(dates_between(*dates))
        self._total = len(self._dates)
        self._current_date = None

    @property
    def page(self):
        return self._current_date

    @property
    def size(self):
        return 1

    @property
    def total(self):
        return self._total

    @property
    def next_page_params(self):
        if self._current_date:
            return {
                'date_gte': self._current_date,
                'date_lte': self._current_date
            }
        return None

    def load(self, params):
        while True:
            response = self.session.get(self.url, headers=self.headers, params=params, timeout=self.timeout)
            if response.status_code == 429:
                retry_after = response.headers.get('Retry-After')
                sleep_time = int(retry_after) if retry_after and retry_after.isdigit() else 60
                print(f"Rate limit hit. Sleeping for {sleep_time} seconds...")
                time.sleep(sleep_time)
                continue
            elif response.status_code != 200:
                response.raise_for_status()
            return response.json()

    def parse(self):
        data = self._raw.get('results', [])
        parsed = []
        for item in data:
            review = {
                'date': self._current_date,
                'author': item.get('author', 'N/A'),
                'created_in_catalog': item.get('created_in_catalog', 'N/A'),
                'created_in_rd': item.get('created_in_rd', 'N/A'),
                'parsed_at': item.get('parsed_at', 'N/A'),
                'comment': item.get('comment', 'N/A'),
                'rating': item.get('rating', 'N/A'),
                'review_id': item.get('id', 'N/A'),
                'origin_url': item.get('origin_url', 'N/A'),
                'location_url': item.get('location_url', 'N/A'),
                'company_name': item.get('company', {}).get('name', 'N/A'),
                'company_code': item.get('company', {}).get('code', 'N/A'),
                'company_country': item.get('company', {}).get('address', {}).get('country', 'N/A'),
                'company_region': item.get('company', {}).get('address', {}).get('region', 'N/A'),
                'company_city': item.get('company', {}).get('address', {}).get('city', 'N/A'),
                'company_street': item.get('company', {}).get('address', {}).get('street', 'N/A'),
                'company_housenumber': item.get('company', {}).get('address', {}).get('housenumber', 'N/A'),
                'company_postcode': item.get('company', {}).get('address', {}).get('postcode', 'N/A'),
                'brand_name': item.get('brand', {}).get('name', 'N/A'),
                'brand_is_test': item.get('brand', {}).get('is_test', 'N/A'),
                'able_to_reply': item.get('able_to_reply', 'N/A'),
                'able_to_abuse': item.get('able_to_abuse', 'N/A'),
                'tags': item.get('tags', 'N/A'),
                'is_changed': item.get('is_changed', 'N/A'),
                'catalog_id': item.get('catalog_id', 'N/A')
            }
            children = item.get('children', [])
            reviews = [] if children else [review]
            for reply in children:
                rep = {
                    'reply_author': reply.get('author', 'N/A'),
                    'reply_comment': reply.get('comment', 'N/A'),
                    'reply_created_in_catalog': reply.get('created_in_catalog', 'N/A'),
                    'reply_created_in_rd': reply.get('created_in_rd', 'N/A'),
                    'reply_parsed_at': reply.get('parsed_at', 'N/A'),
                    'is_company_comment': reply.get('is_company_comment', 'N/A'),
                    'is_autoreply': reply.get('is_autoreply', 'N/A'),
                    'able_to_edit': reply.get('able_to_edit', 'N/A'),
                    'able_to_delete': reply.get('able_to_delete', 'N/A'),
                }
                reviews.append(review | rep)
            parsed.extend(reviews)
        return parsed

    def __iter__(self):
        """
        Iterator that goes through each day in the given date range.
        For each date, it loads the corresponding data, parses it, updates stats,
        and then yields the parsed data.
        """
        self._start_date = datetime.now()
        while self._dates:
            self._current_date = self._dates.popleft()
            try:
                self._raw = self.load(self.next_page_params)
                data = self.parse()
                self._parsed_count = self.total - len(self._dates)
                self._end_date = datetime.now()
                yield data
            except (ReadTimeout, ConnectTimeout):
                print("Timeout occurred. Waiting before retrying...")
                time.sleep(self.timeout)
        # Iteration complete


if __name__ == '__main__':
    review = {"name": "test"}
    replies = [{"id": "a"}, {"id": "b"}]
    result = []
    if result:
        print("test")
    for reply in replies:
        result.append(review | reply)

    print(result)