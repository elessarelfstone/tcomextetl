import pytest

from tcomextetl.extract.kgd_requests import KgdGovKzSoapApiParser
from tests.fixtures.fixt_kgdgov import fixture_kgdgov_tax_payments_success


def test_kgdgov_taxpayments_success(fixture_kgdgov_tax_payments_success):
    xml, data = fixture_kgdgov_tax_payments_success
    parser = KgdGovKzSoapApiParser(None, None)
    parser.raw = xml
    assert parser.parse() == data



