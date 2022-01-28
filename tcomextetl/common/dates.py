from datetime import datetime

DEFAULT_FORMAT = '%Y-%m-%d'


def today(frmt=DEFAULT_FORMAT):
    return datetime.today().strftime(frmt)



