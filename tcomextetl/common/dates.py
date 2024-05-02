from calendar import monthrange
from datetime import date, datetime, timedelta

DEFAULT_FORMAT = '%Y-%m-%d'
DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DEFAULT_MONTH_FORMAT = '%Y-%m'
DEFAULT_DATETIME_FORMAT_WITHT = "%Y-%m-%dT%H:%M:%S"


def today():
    return datetime.today()


def first_day_of_month() -> date:
    _date = datetime.today()
    return _date.replace(day=1)


def last_day_of_month() -> date:
    _date = datetime.today()
    return _date.replace(monthrange(_date.year, _date.month)[1])


def yesterday(frmt=DEFAULT_FORMAT):
    y = datetime.today() - timedelta(days=1)
    return y.strftime(frmt)


def n_days_ago(n: int = 1):
    return datetime.today() - timedelta(days=n)


def previous_month():
    t = date.today()
    ld = date(t.year, t.month, 1) - timedelta(days=1)
    return '{}-{:02}'.format(ld.year, ld.month)


def month_as_range(month):
    d = datetime.strptime(month, DEFAULT_MONTH_FORMAT)
    return d.date(), date(d.year, d.month, monthrange(d.year, d.month)[1])


def first_day_of_previous_month() -> date:
    _date = datetime.today()
    first_day_of_current_month = _date.replace(day=1)
    last_day_previous_month = first_day_of_current_month - timedelta(days=1)
    first_day_previous_month = last_day_previous_month.replace(day=1)
    return first_day_previous_month.date()


def last_day_of_previous_month() -> date:
    _date = datetime.today()
    first_day_of_current_month = _date.replace(day=1)
    last_day_previous_month = first_day_of_current_month - timedelta(days=1)
    return last_day_previous_month.date()


def dates_between(start_date, end_date) -> [date]:
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)

    return dates
