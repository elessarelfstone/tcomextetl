import os

from dotenv import load_dotenv

load_dotenv()

DATA_PATH = os.getenv('DATA_PATH')
TEMP_PATH = os.getenv('TEMP_PATH')
PARAMS_CONFIG_PATH = os.getenv('PARAMS_CONFIG_PATH')
TBOT_TOKEN = os.getenv('TBOT_TOKEN')
TBOT_CHAT_IDS = os.getenv('TBOT_CHAT_IDS')


FTP_PATH = os.getenv('FTP_PATH')
FTP_HOST = os.getenv('FTP_HOST')
FTP_USER = os.getenv('FTP_USER')
FTP_PASS = os.getenv('FTP_PASS')
FTP_EXPORT_PATH = os.getenv('FTP_EXPORT_PATH')

GOSZAKUP_TOKEN = os.getenv('GOSZAKUP_TOKEN')
# GOSZAKUP_N_DAYS_DELTA = os.getenv('GOSZAKUP_N_DAYS_DELTA')

KGD_SOAP_TOKEN = os.getenv('KGD_SOAP_TOKEN')

DATAGOV_TOKEN = os.getenv('DATAGOV_TOKEN')

SAMRUK_API_HOST = os.getenv('SAMRUK_API_HOST')
SAMRUK_USER = os.getenv('SAMRUK_USER')
SAMRUK_PASSWORD = os.getenv('SAMRUK_PASSWORD')
SAMRUK_API_COMPANY_ID = os.getenv('SAMRUK_API_COMPANY_ID')


INFOBIP_USER = os.getenv('INFOBIP_USER')
INFOBIP_PASSWORD = os.getenv('INFOBIP_PASSWORD')
INFOBIP_TIMEOUT = os.getenv('INFOBIP_API_TIMEOUT')
INFOBIP_DRB_TOKEN = os.getenv('INFOBIP_DRB_TOKEN')


TELECOMOBKZ_YANDEX_APP_METRICA_TOKEN = os.getenv('TELECOMOBKZ_YANDEX_APP_METRICA_TOKEN')
TELECOMKZ_YANDEX_METRICA_TOKEN = os.getenv('TELECOMKZ_YANDEX_METRICA_TOKEN')
TELECOMKZ_YANDEX_METRICA_LOGS_YAM2_TOKEN = os.getenv('TELECOMKZ_YANDEX_METRICA_LOGS_YAM2_TOKEN')
TELECOMKZ_YANDEX_METRICA_LOGS_TERMINAL_TOKEN = os.getenv('TELECOMKZ_YANDEX_METRICA_LOGS_TERMINAL_TOKEN')
TELECOMKZ_YANDEX_METRICA_LOGS_REDESIGN_TOKEN = os.getenv('TELECOMKZ_YANDEX_METRICA_LOGS_REDESIGN_TOKEN')
TELECOMKZ_YANDEX_METRICA_LOGS_WFM_TOKEN = os.getenv('TELECOMKZ_YANDEX_METRICA_LOGS_WFM_TOKEN')

SPEEDTEST_USER = os.getenv('SPEEDTEST_USER')
SPEEDTEST_PASS = os.getenv('SPEEDTEST_PASS')

CRMSENSOR_USER = os.getenv('CRMSENSOR_USER')
CRMSENSOR_PASS = os.getenv('CRMSENSOR_PASS')


IOT_TOKEN = os.getenv('IOT_TOKEN')

SAMRUK_TOKEN = os.getenv('SAMRUK_TOKEN')

MIRAPOLIS_SECRET_KEY = os.getenv('MIRAPOLIS_SECRET_KEY')

AITU_API_KEY = os.getenv('AITU_API_KEY')
AITU_SECRET_KEY = os.getenv('AITU_SECRET_KEY')

AITU_PUSH_NOTIFICATIONS_PROJECT_ID = os.getenv('AITU_PUSH_NOTIFICATIONS_PROJECT_ID')
AITU_PUSH_NOTIFICATIONS_PRIVATE_KEY_ID = os.getenv('AITU_PUSH_NOTIFICATIONS_PRIVATE_KEY_ID')
AITU_PUSH_NOTIFICATIONS_PRIVATE_KEY = os.getenv('AITU_PUSH_NOTIFICATIONS_PRIVATE_KEY')
AITU_PUSH_NOTIFICATIONS_CLIENT_ID = os.getenv('AITU_PUSH_NOTIFICATIONS_CLIENT_ID')

AMPLITUDE_EGOV_LOGS_API_KEY = os.getenv('AMPLITUDE_EGOV_LOGS_API_KEY')
AMPLITUDE_EGOV_LOGS_SECRET_KEY = os.getenv('AMPLITUDE_EGOV_LOGS_SECRET_KEY')
AMPLITUDE_TELECOMKZ_LOGS_API_KEY = os.getenv('AMPLITUDE_TELECOMKZ_LOGS_API_KEY')
AMPLITUDE_TELECOMKZ_LOGS_SECRET_KEY = os.getenv('AMPLITUDE_TELECOMKZ_LOGS_SECRET_KEY')