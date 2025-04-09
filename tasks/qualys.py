import ipaddress
import logging
import os
import json
import xml.etree.ElementTree as ET

import luigi
import numpy as np
from luigi.parameter import ParameterVisibility
from luigi.util import requires
from requests.auth import HTTPBasicAuth

from tasks.base import FtpUploadedOutput, Runner, ApiToCsv, ExternalFtpCsvDFInput
from tcomextetl.common.dates import today
from tcomextetl.common.csv import save_csvrows, dict_to_row
from tcomextetl.common.utils import rewrite_file, read_csv_tuples
from settings import QUALYS_API_USER, QUALYS_API_PASSWORD
from tcomextetl.extract.qualys_requests import QualysDataRequest

QUALYS_API_BASE_URL = "https://qualysapi.qualys.eu/api/2.0/fo"

DEFAULT_PARAMS = {
    'action': 'list',
    'show_tags': '1',
    'show_qds': '1',
    'truncation_limit': '0',
    'status': 'New, Active, Re-Opened, Fixed',
    'severities': '1,2,3,4,5',
    'include_ignored': '1',
    'include_disabled': '1',
}

ACS_DICT = {
    "Internet Facing Assets": 5.0,
    "Active Directory": 5.0,
    "DIT": 5.0,
    "CloudVideoControl": 4.0,
    "Domain Controller": 4.0,
    "CORP IP": 4.0,
    "EXTERNAL IP": 4.0,
    "CORP IP for Astana scanner": 4.0,
    "CORP IP for Almaty scanner": 4.0,
    "CORP IP for Pavlodar scanner": 4.0,
    "CORP IP for Low Performance scan": 4.0,
    "ismet.kz": 5.0,
    "ODS Networks": 5.0,
    "Big Data": 5.0,
    "ACS-5": 5.0,
    "ACS-4": 4.0,
    "ACS-3": 3.0,
    "ACS-2": 2.0,
    "ACS-1": 1.0,
    "[BDCS] BLOCK FOR DEVELOPMENT OF CORPORATE SYSTEMS": 5.0,
    "ODS": 5.0,
    "DTK": 5.0,
    "BLOCK GR": 5.0,
    "OSS_and_IT": 3.0
}


class QidManager:

    def __init__(self, qids_fpath, username, password, endpoint_qid_info):

        self.logger = logging.getLogger(self.__class__.__name__)
        self.qids_fpath = qids_fpath
        self.username = username
        self.password = password
        self.endpoint_qid_info = endpoint_qid_info
        self.qids_dict = {}

        try:
            self.qids = read_csv_tuples(qids_fpath, delimiter=';')

            for qid, title in self.qids:
                self.qids_dict[qid.strip()] = title.strip()

            self._qids_count = len(self.qids_dict)

        except Exception as e:
            self.logger.error(f"Error loading QIDs from file {qids_fpath}: {e}")

    @property
    def url_qid_info_base(self):
        return f'{QUALYS_API_BASE_URL}{self.endpoint_qid_info}'

    def total(self):
        return self._qids_count

    @property
    def headers(self):
        return {'X-Requested-With': 'QualysPostman'}

    @property
    def request_params(self):
        return DEFAULT_PARAMS

    def get_title(self, qid):

        str_qid = str(qid)
        title = self.qids_dict.get(str_qid)

        if title is None:
            try:
                title = self.get_qid_info(str_qid)

                if title != "N/A":
                    self.qids_dict[str_qid] = title
                    self.logger.info(f"Updated dictionary with new QID {str_qid}: {title}")
                    self._qids_count = len(self.qids_dict)

            except Exception as e:
                self.logger.error(f"Error updating QID dictionary: {e}")

        return title

    def get_qid_info(self, qid):

        qid_url = f"{self.url_qid_info_base}{qid}"

        try:
            request = QualysDataRequest(
                url=qid_url,
                headers=self.headers,
                auth=HTTPBasicAuth(self.username, self.password),
                params=self.request_params
            )

            xml_text = request.get_qid_info_raw()
            root = ET.fromstring(xml_text)
            title = root.findtext(".//TITLE", default="N/A")
            return title

        except Exception as e:
            self.logger.error(f"Failed to get info for QID {qid}: {e}")
            return "N/A"


class QualysOutput(ApiToCsv):
    username = luigi.Parameter(default=QUALYS_API_USER, visibility=ParameterVisibility.HIDDEN)
    password = luigi.Parameter(default=QUALYS_API_PASSWORD, visibility=ParameterVisibility.HIDDEN)
    endpoint = luigi.Parameter(default="/asset/host/vm/detection/")
    endpoint_qid_info = luigi.Parameter(default="/knowledge_base/vuln/?action=list&ids=")
    from_to = luigi.TupleParameter(default=())
    ftp_file_mask = luigi.Parameter()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.qid_manager = None
        self.parsed_cnt = 0

    @property
    def dates_params(self):
        params = dict()
        params['date_from'], params['date_to'] = self.from_to
        return params

    @property
    def qids_fpath(self):
        return self._file_path('.qids')

    @property
    def url(self):
        return f'{QUALYS_API_BASE_URL}{self.endpoint}'

    @property
    def request_params(self):
        return DEFAULT_PARAMS

    @property
    def headers(self):
        return {'X-Requested-With': 'QualysPostman'}

    def requires(self):
        return ExternalFtpCsvDFInput(ftp_file_mask=self.ftp_file_mask)

    def parse_xml(self, xml_text):

        try:
            root = ET.fromstring(xml_text)
            processed_data = []

            qids_manager = QidManager(
                self.qids_fpath,
                self.username,
                self.password,
                self.endpoint_qid_info)

            wc = 1.0
            wh = 0.6
            wm = 0.4
            wl = 0.2
            for host in root.findall(".//HOST"):

                ACS = []
                QDSc = []
                QDSh = []
                QDSm = []
                QDSl = []

                asset_ipv4 = host.findtext("IP", default="N/A")
                asset_name = host.findtext(".//DNS_DATA/FQDN", default="N/A")
                asset_tag_elements = host.findall(".//TAGS/TAG")
                asset_tag_names = [tag.findtext("NAME", default="N/A") for tag in asset_tag_elements]

                for tag_name in asset_tag_names:
                    criticality_score = ACS_DICT.get(tag_name, 2)
                    ACS.append(criticality_score)

                asset_tags = ", ".join(asset_tag_names)
                external = False if ipaddress.ip_address(asset_ipv4).is_private else True

                for detection in host.findall(".//DETECTION"):
                    qid = detection.findtext("QID", default="N/A")

                    title = qids_manager.get_title(qid)
                    if not title:
                        title = qids_manager.get_qid_info(qid)

                    status = detection.findtext("STATUS", default="N/A")
                    severity = detection.findtext("SEVERITY", default="N/A")

                    disabled = "Yes" if detection.findtext("IS_DISABLED", "0") == "1" else "No"
                    ignored = "Yes" if detection.findtext("IS_IGNORED", "0") == "1" else "No"

                    qds_element = detection.find("QDS")
                    qds_value = qds_element.text if qds_element is not None else "N/A"
                    qds_severity = qds_element.get("severity", "N/A") if qds_element is not None else "N/A"

                    if status.lower() != 'fixed' and disabled.lower() == 'no' and ignored.lower() == 'no':
                        if qds_severity == 'CRITICAL':
                            QDSc.append(int(qds_value))
                        elif qds_severity == 'HIGH':
                            QDSh.append(int(qds_value))
                        elif qds_severity == 'MEDIUM':
                            QDSm.append(int(qds_value))
                        elif qds_severity == 'LOW':
                            QDSl.append(int(qds_value))

                    if len(ACS) == 0:
                        trurisk_score = self.calculate_trurisk_score(2, wc, QDSc, wh, QDSh, wm, QDSm, wl, QDSl,
                                                                     external)
                    else:
                        trurisk_score = self.calculate_trurisk_score(max(ACS), wc, QDSc, wh, QDSh, wm, QDSm, wl, QDSl,
                                                                     external)

                    detection_data = {
                        "qid": qid,
                        "title": title,
                        "severity": severity,
                        "last_detected": detection.findtext("LAST_FOUND_DATETIME", default="N/A"),
                        "first_detected": detection.findtext("FIRST_FOUND_DATETIME", default="N/A"),
                        "status": status,
                        "asset_name": asset_name,
                        "asset_ipv4": asset_ipv4,
                        "asset_tags": asset_tags,
                        "disabled": disabled,
                        "ignored": ignored,
                        "qds": qds_value,
                        "qds_severity": qds_severity,
                        "true_risk_score": trurisk_score
                    }

                    processed_data.append(detection_data)

            return processed_data

        except ET.ParseError as e:
            self.logger.error(f"XML parsing error: {e}")
            raise

    @staticmethod
    def calculate_trurisk_score(ACS, wc, QDSc, wh, QDSh, wm, QDSm, wl, QDSl, external):

        Avg_QDSc = np.nanmean(QDSc) if len(QDSc) > 0 else 0
        Avg_QDSh = np.nanmean(QDSh) if len(QDSh) > 0 else 0
        Avg_QDSm = np.nanmean(QDSm) if len(QDSm) > 0 else 0
        Avg_QDSl = np.nanmean(QDSl) if len(QDSl) > 0 else 0

        Count_QDSc = len(QDSc)
        Count_QDSh = len(QDSh)
        Count_QDSm = len(QDSm)
        Count_QDSl = len(QDSl)

        term1 = wc * Avg_QDSc * np.power(Count_QDSc, 1 / 100) if Count_QDSc > 0 else 0
        term2 = wh * Avg_QDSh * np.power(Count_QDSh, 1 / 100) if Count_QDSh > 0 else 0
        term3 = wm * Avg_QDSm * np.power(Count_QDSm, 1 / 100) if Count_QDSm > 0 else 0
        term4 = wl * Avg_QDSl * np.power(Count_QDSl, 1 / 100) if Count_QDSl > 0 else 0

        total_score = term1 + term2 + term3 + term4

        if external:
            trurisk_score = ACS * total_score * 1.2
        else:
            trurisk_score = ACS * total_score

        trurisk_score = min(trurisk_score, 1000)

        return trurisk_score

    def run(self):
        if not os.path.exists(self.qids_fpath):
            self.input().get(str(self.qids_fpath))

        # Create request object
        request = QualysDataRequest(
            url=self.url,
            headers=self.headers,
            auth=HTTPBasicAuth(self.username, self.password),
            params=self.request_params,
            date_params=self.dates_params
        )

        raw_xml = request.get_raw_data()
        rows = self.parse_xml(raw_xml)
        data = []

        if rows:
            for row in rows:
                try:
                    # Преобразуем словарь в строку для CSV
                    row_data = dict_to_row(row, self.struct)
                    data.append(row_data)
                    self.parsed_cnt += 1
                except Exception as e:
                    continue

        save_csvrows(self.output_fpath, data, quotechar='"')
        stat = request.stat
        stat.update({'name': self.name})
        stat.update({'parsed': self.parsed_cnt})
        rewrite_file(self.stat_fpath, json.dumps(stat))

        self.finalize()


@requires(QualysOutput)
class QualysFtpOutput(FtpUploadedOutput):
    pass


class QualysVulnerabilitiesRunner(Runner):
    start_date = luigi.DateParameter(default=today())
    end_date = luigi.DateParameter(default=today())

    @property
    def params(self):
        params = super(QualysVulnerabilitiesRunner, self).params

        params['from_to'] = (
            self.start_date.isoformat(),
            self.end_date.isoformat()
        )

        return params

    def requires(self):
        return QualysFtpOutput(
            **self.params
        )


class QualysVulnerabilities(QualysVulnerabilitiesRunner):
    name = luigi.Parameter('qualys_vulnerabilities')


if __name__ == '__main__':
    luigi.run()
