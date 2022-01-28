from tcomextetl.transform.sgov import *
from tcomextetl.transform.kgd import *


class StructRegister:

    _handlers = {}

    @classmethod
    def add(cls, name, handler):
        cls._handlers[name] = handler

    @classmethod
    def get(cls, name):
        try:
            return cls._handlers[name]
        except KeyError:
            raise ValueError(name)


# stat.gov.kz
StructRegister.add('sgov_oked', OkedRow)
StructRegister.add('sgov_kato', KatoRow)
StructRegister.add('sgov_mkeis', MkeisRow)
StructRegister.add('sgov_kurk', KurkRow)
StructRegister.add('sgov_kpved', KpvedRow)
StructRegister.add('sgov_companies', CompanieRow)

# kgd.gov.kz
StructRegister.add('kgd_bankrupt', BankruptRow)
StructRegister.add('kgd_inactive', InactiveRow)
StructRegister.add('kgd_invregistration', InvregistrationRow)
StructRegister.add('kgd_jwaddress', JwaddressRow)
StructRegister.add('kgd_pseudocompany', PseudocompanyRow)
StructRegister.add('kgd_taxarrears150', TaxArrears150Row)
StructRegister.add('kgd_taxviolators', TaxViolatorsRow)










