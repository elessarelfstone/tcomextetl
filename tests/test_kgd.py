import pytest

from tcomextetl.extract.kgdgov_requests import KgdGovKzSoapApiParser
from tests.fixtures.kgdgov import fixture_kgdgov_tax_payments_success


def test_kgdgov_taxpayments_success(fixture_kgdgov_tax_payments_success):
    xml, data = fixture_kgdgov_tax_payments_success
    parser = KgdGovKzSoapApiParser(None, None, None)
    parser.raw = xml
    assert parser.parse() == data



