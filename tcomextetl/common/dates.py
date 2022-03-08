from datetime import datetime, timedelta

DEFAULT_FORMAT = '%Y-%m-%d'


def today(frmt=DEFAULT_FORMAT):
    return datetime.today().strftime(frmt)


def yesterday(frmt=DEFAULT_FORMAT):
    y = datetime.today() - timedelta(days=1)
    return y.strftime(frmt)
