from pathlib import Path

import pytest

from tcomextetl.common.utils import read_file

response_xml_dir = Path(__file__).parent.parent / 'misc' / 'kgdgov'


@pytest.fixture()
def fixture_kgdgov_tax_payments_success():
    xml = read_file(response_xml_dir / 'tax_payments_success.xml')
    data = [
        {
            'bin': '012345678901',
            'TaxOrgCode': '451501',
            'NameTaxRu': 'UGD Astana Ru',
            'NameTaxKz': 'UGD Astana Kz',
            'KBK': '103101',
            'KBKNameRu': 'Social Tax Ru',
            'KBKNameKz': 'Social Tax Kz',
            'PayNum': '2',
            'PayType': '1',
            'EntryType': '1',
            'ReceiptDate': '2022-01-01+06:00',
            'WriteOffDate': '2022-01-02+06:00',
            'Summa': '15646'
        }
        ,
        {
            'bin': '012345678901',
            'TaxOrgCode': '451501',
            'NameTaxRu': 'UGD Almaty Ru',
            'NameTaxKz': 'UGD Almaty Kz',
            'KBK': '101201',
            'KBKNameRu': 'Individual Tax Ru',
            'KBKNameKz': 'Individual Tax Kz',
            'PayNum': '1',
            'PayType': '1',
            'EntryType': '1',
            'ReceiptDate': '2022-01-12+06:00',
            'WriteOffDate': '2022-01-12+06:00',
            'Summa': '17926'
        }
    ]

    return xml, data
