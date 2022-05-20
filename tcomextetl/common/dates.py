from calendar import monthrange
from datetime import date, datetime, timedelta

DEFAULT_FORMAT = '%Y-%m-%d'
DEFAULT_MONTH_FORMAT = '%Y-%m'


def today(frmt=DEFAULT_FORMAT):
    return datetime.today().strftime(frmt)


def yesterday(frmt=DEFAULT_FORMAT):
    y = datetime.today() - timedelta(days=1)
    return y.strftime(frmt)


def previous_month():
    t = date.today()
    ld = date(t.year, t.month, 1) - timedelta(days=1)
    return '{}-{:02}'.format(ld.year, ld.month)


def month_as_range(month):
    d = datetime.strptime(month, DEFAULT_MONTH_FORMAT)
    return d.replace(day=1), date(d.year, d.month, monthrange(d.year, d.month)[1])
