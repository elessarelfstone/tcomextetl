import csv
import json
from math import floor
from datetime import datetime, timedelta
from time import sleep

import luigi
import pandas as pd
from luigi.parameter import ParameterVisibility
from luigi.util import requires

from tasks.base import CsvFileOutput, FtpUploadedOutput, Runner
from tcomextetl.common.arch import extract_by_wildcard
from tcomextetl.common.csv import save_csvrows, dict_to_row, CSV_QUOTECHAR
from tcomextetl.common.dates import DEFAULT_FORMAT, n_days_ago
from tcomextetl.common.utils import build_fpath, append_file, rewrite_file
from settings import AMPLITUDE_EGOV_LOGS_API_KEY, AMPLITUDE_EGOV_LOGS_SECRET_KEY, AMPLITUDE_TELECOMKZ_LOGS_API_KEY, \
    AMPLITUDE_TELECOMKZ_LOGS_SECRET_KEY

