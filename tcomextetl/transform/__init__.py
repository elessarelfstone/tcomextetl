from tcomextetl.transform.sgov import *
from tcomextetl.transform.kgd import *
from tcomextetl.transform.goszakup import *
from tcomextetl.transform.dgov import *
from tcomextetl.transform.samruk import *
from tcomextetl.transform.infobip import *
from tcomextetl.transform.telecomobkz import *
from tcomextetl.transform.telecomkz import *
from tcomextetl.transform.speedtest import *
from tcomextetl.transform.crmsensor import *
from tcomextetl.transform.iot import *


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
StructRegister.add('sgov_active_companies', CompanieRow)
StructRegister.add('sgov_active_legal_entities', CompanieRow)
StructRegister.add('sgov_active_foreign_branches', CompanieRow)
StructRegister.add('sgov_active_joint_ventures', CompanieRow)
StructRegister.add('sgov_active_entrepreneurs', CompanieRow)
StructRegister.add('sgov_active_legal_branches', CompanieRow)


# kgd.gov.kz
StructRegister.add('kgd_bankrupt', BankruptRow)
StructRegister.add('kgd_inactive', InactiveRow)
StructRegister.add('kgd_invregistration', InvregistrationRow)
StructRegister.add('kgd_jwrongaddress', JwaddressRow)
StructRegister.add('kgd_pseudocompany', PseudocompanyRow)
StructRegister.add('kgd_taxarrears150', TaxArrears150Row)
StructRegister.add('kgd_taxviolators', TaxViolatorsRow)
StructRegister.add('kgd_taxpayments', TaxPaymentsRow)

# goszakup_dags.gov.kz
StructRegister.add('goszakup_companies', GoszakupCompanyRow)
StructRegister.add('goszakup_contracts', GoszakupContractRow)
StructRegister.add('goszakup_untrusted', GoszakupUntrustedSupplierRow)
StructRegister.add('goszakup_lots', GoszakupLotsRow)
StructRegister.add('goszakup_trd_buys', GoszakupTradeBuyRow)
StructRegister.add('goszakup_plan_points', GoszakupPlanPointRow)
StructRegister.add('goszakup_plans_kato', GoszakupPlanKatoRow)
StructRegister.add('goszakup_contract_units', GoszakupContractUnitsRow)
StructRegister.add('goszakup_trd_app_offers', GoszakupTrdAppOffersRow)


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
StructRegister.add('samruk_certs', SamrukCertRow)
StructRegister.add('samruk_dicts', SamrukDictRow)


# infobip
StructRegister.add('infobip_agents', InfobipAgentRow)
StructRegister.add('infobip_queues', InfobipQueueRow)
StructRegister.add('infobip_conversations', InfobipConversationRow)
StructRegister.add('infobip_messages', InfobipConvMessagesRow)
StructRegister.add('infobip_tags', InfobipConvTagsRow)


# telecomobkz
StructRegister.add('telecomobkz_logs_clicks', TelecomobkzClickLogRow)
StructRegister.add('telecomobkz_logs_installations', TelecomobkzInstallationLogRow)
StructRegister.add('telecomobkz_logs_postbacks', TelecomobkzPostbackLogRow)
StructRegister.add('telecomobkz_reps_acquisitions', TelecomobkzRepAcquisitionsRow)
StructRegister.add('telecomobkz_reps_dau', TelecomobkzRepDauRow)
StructRegister.add('telecomobkz_reps_events', TelecomobkzRepEventRow)


# telecomkz
StructRegister.add('telecomkz_reps_main_visits', TelecomkzMainVisitsRow)
StructRegister.add('telecomkz_reps_main_users', TelecomkzMainUsersRow)
StructRegister.add('telecomkz_reps_lk1_visits', TelecomkzLK1VisitsRow)
StructRegister.add('telecomkz_reps_lk1_users', TelecomkzLK1UsersRow)
StructRegister.add('telecomkz_reps_lk2_visits', TelecomkzLK2VisitsRow)
StructRegister.add('telecomkz_reps_lk2_users', TelecomkzLK2UsersRow)
StructRegister.add('telecomkz_reps_lk2_yam2_visits', TelecomkzLK2Yam2VisitsRow)
StructRegister.add('telecomkz_reps_lk2_yam2_users', TelecomkzLK2Yam2UsersRow)

# telecomob
StructRegister.add('speedtest_sensitive_data', SpeedtestSensitiveDataRow)
StructRegister.add('speedtest_fixed_network_performance', FixedNetworkPerformanceRow)

# crmsensor
StructRegister.add('crmsensor_checklist', CrmsensorChecklistRow)


StructRegister.add('iot_stat', IotStatRow)
