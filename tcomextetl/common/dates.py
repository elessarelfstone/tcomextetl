from calendar import monthrange
from datetime import date, datetime, timedelta

DEFAULT_FORMAT = '%Y-%m-%d'
DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DEFAULT_MONTH_FORMAT = '%Y-%m'


def today():
    return datetime.today()


def first_day_of_month() -> date:
    _date = datetime.today()
    return _date.replace(day=1)


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
