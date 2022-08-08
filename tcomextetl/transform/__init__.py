from tcomextetl.transform.sgov import *
from tcomextetl.transform.kgd import *
from tcomextetl.transform.goszakup import *
from tcomextetl.transform.dgov import *
from tcomextetl.transform.samruk import *


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
StructRegister.add('sgov_legal_entities', CompanieRow)
StructRegister.add('sgov_foreign_branches', CompanieRow)
StructRegister.add('sgov_joint_ventures', CompanieRow)
StructRegister.add('sgov_entrepreneurs', CompanieRow)
StructRegister.add('sgov_legal_branches', CompanieRow)


# kgd.gov.kz
StructRegister.add('kgd_bankrupt', BankruptRow)
StructRegister.add('kgd_inactive', InactiveRow)
StructRegister.add('kgd_invregistration', InvregistrationRow)
StructRegister.add('kgd_jwaddress', JwaddressRow)
StructRegister.add('kgd_pseudocompany', PseudocompanyRow)
StructRegister.add('kgd_taxarrears150', TaxArrears150Row)
StructRegister.add('kgd_taxviolators', TaxViolatorsRow)
StructRegister.add('kgd_taxpayments', TaxPaymentsRow)

# goszakup.gov.kz
StructRegister.add('goszakup_companies', GoszakupCompanyRow)
StructRegister.add('goszakup_contracts', GoszakupContractRow)
StructRegister.add('goszakup_untrusted', GoszakupUntrustedSupplierRow)
StructRegister.add('goszakup_lots', GoszakupLotsRow)
StructRegister.add('goszakup_trd_buys', GoszakupTradeBuyRow)
StructRegister.add('goszakup_plan_points', GoszakupPlanPointRow)
StructRegister.add('goszakup_plans_kato', GoszakupPlanKatoRow)
StructRegister.add('goszakup_contract_units', GoszakupContractUnitsRow)


# data.egov.kz
StructRegister.add('dgov_addrreg_dats_types', DgovAddrRegDAtsTypes)
StructRegister.add('dgov_addrreg_dbuildings_pointers', DgovAddrRegDBuildingsPointers)
StructRegister.add('dgov_addrreg_dgeonims_types', DgovAddrRegDGeonimsTypes)
StructRegister.add('dgov_addrreg_drooms_types', DgovAddrRegDRoomsTypes)

StructRegister.add('dgov_addrreg_sats', DgovAddrRegSAtsRow)
StructRegister.add('dgov_addrreg_sgeonims', DgovAddrRegSGeonimsRow)
StructRegister.add('dgov_addrreg_sgrounds', DgovAddrRegSGroundsRow)
StructRegister.add('dgov_addrreg_sbuildings', DgovAddrRegSBuildingsRow)
StructRegister.add('dgov_addrreg_spb', DgovAddrRegSPbRow)

# samruk
StructRegister.add('samruk_suppliers', SamrukSupplierRow)
StructRegister.add('samruk_bad_suppliers', SamrukBadSupplierRow)
StructRegister.add('samruk_kzt_purchases', SamrukPurchaseRow)
StructRegister.add('samruk_kzt_contracts', SamrukKztContractRow)
StructRegister.add('samruk_kzt_contract_subjects', SamrukKztContractSubjectsRow)
StructRegister.add('samruk_kzt_plans', SamrukKztPlanRow)
StructRegister.add('samruk_kzt_plan_items', SamrukKztPlanItemRow)



