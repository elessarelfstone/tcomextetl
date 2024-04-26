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
from tcomextetl.transform.mirapolis import *
from tcomextetl.transform.aitu import *
from tcomextetl.transform.gosreestrkz import *
from tcomextetl.transform.cloudpayments import *
from tcomextetl.transform.amplitude import *
from tcomextetl.transform.tvplus import *


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

StructRegister.add('goszakup_lots_status', GoszakupLotsStatusRow)
StructRegister.add('goszakup_ref_trade_methods', GoszakupRefTradeMethodsRow)
StructRegister.add('goszakup_ref_pln_point_status', GoszakupRefPlnPointStatusRow)
StructRegister.add('goszakup_ref_subject_type', GoszakupRefSubjectTypeRow)
StructRegister.add('goszakup_ref_buy_status', GoszakupRefBuyStatusRow)
StructRegister.add('goszakup_ref_po_st', GoszakupRefPriceOfferStatusRow)
StructRegister.add('goszakup_ref_kato', GoszakupRefKatoRow)
StructRegister.add('goszakup_ref_justification', GoszakupRefJustificationRow)
StructRegister.add('goszakup_ref_type_trade', GoszakupRefTypeTradeRow)
StructRegister.add('goszakup_ref_contract_status', GoszakupRefContractStatusRow)

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
StructRegister.add('samruk_purchases', SamrukPurchaseRow)
StructRegister.add('samruk_contracts', SamrukKztContractRow)
StructRegister.add('samruk_contract_items', SamrukContractItemsRow)
StructRegister.add('samruk_plans', SamrukPlanRow)
StructRegister.add('samruk_plan_items', SamrukPlanItemRow)
StructRegister.add('samruk_contract_item_deliveries', SamrukContractItemDeliveries)
StructRegister.add('samruk_dicts', SamrukDictRow)
StructRegister.add('samruk_entries', SamrukEntriesRow)
StructRegister.add('samruk_participation_lots', SamrukParticipationLotRow)


# infobip
StructRegister.add('infobip_agents', InfobipAgentRow)
StructRegister.add('infobip_queues', InfobipQueueRow)
StructRegister.add('infobip_conversations', InfobipConversationRow)
StructRegister.add('infobip_messages', InfobipConvMessagesRow)
StructRegister.add('infobip_tags', InfobipConvTagsRow)

StructRegister.add('infobip_omni_agents', InfobipAgentRow)
StructRegister.add('infobip_omni_queues', InfobipQueueRow)
StructRegister.add('infobip_omni_conversations', InfobipConversationRow)
StructRegister.add('infobip_omni_messages', InfobipConvMessagesRow)
StructRegister.add('infobip_omni_tags', InfobipConvTagsRow)

# telecomobkz
StructRegister.add('telecomobkz_logs_profiles', TelecomobkzProfileLogRow)
StructRegister.add('telecomobkz_logs_events', TelecomobkzEventLogRow)
StructRegister.add('telecomobkz_logs_crashes', TelecomobkzCrashLogRow)
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
StructRegister.add('telecomkz_reps_conversions_main', TelecomkzConversionsMainRow)
StructRegister.add('telecomkz_reps_conversions_lk1', TelecomkzConversionsLK1Row)
StructRegister.add('telecomkz_reps_conversions_lk2', TelecomkzConversionsLK2Row)

StructRegister.add('telecomkz_logs_main_visits', TelecomkzLogsRow)
StructRegister.add('telecomkz_logs_redesign_visits', TelecomkzRedesignLogsRow)
StructRegister.add('telecomkz_logs_redesign2_visits', TelecomkzRedesignLogsRow)
StructRegister.add('telecomkz_logs_wfm_visits', TelecomkzWfmLogsRow)
# speed test
StructRegister.add('speedtest_sensitive_data', SpeedtestSensitiveDataRow)
StructRegister.add('speedtest_fixed_network_performance', FixedNetworkPerformanceRow)

# crmsensor
StructRegister.add('crmsensor_checklist', CrmsensorChecklistRow)

StructRegister.add('iot_stat', IotStatRow)

StructRegister.add('mirapolis_offline_study', MirapolisRow)
StructRegister.add('mirapolis_online_study', MirapolisRow)

StructRegister.add('tvplus_cinema_start', TvPlusCinemaStartRow)
StructRegister.add('tvplus_cinema_kazvod', TvPlusCinemaKazvodRow)
StructRegister.add('tvplus_cinema_megogo', TvPlusCinemaMegogoRow)
StructRegister.add('tvplus_programs', TvPlusProgramsRow)

StructRegister.add('aitu_logs', AituMetricLog)
StructRegister.add('aitu_notifications', AituNotificationMetricLog)

StructRegister.add('gosreestrkz_company', GosreestrKzCompanyRow)
StructRegister.add('gosreestrkz_contact', GosreestrKzContactRow)

StructRegister.add('cloud_payments_list', CloudPaymentsRow)

StructRegister.add('amplitude_egov_logs', AmplitudeEgovLogsRow)
StructRegister.add('amplitude_telecomkz_logs', AmplitudeTelecomkzLogsRow)
