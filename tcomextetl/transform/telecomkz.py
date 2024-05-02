from attrs import define, field


@define
class TelecomkzMainVisitsRow:
    date = field(default='')
    sess_count = field(default='')


@define
class TelecomkzMainUsersRow:
    date = field(default='')
    user_count = field(default='')


@define
class TelecomkzLK1VisitsRow:
    date = field(default='')
    sess_count = field(default='')


@define
class TelecomkzLK1UsersRow:
    date = field(default='')
    user_count = field(default='')


@define
class TelecomkzLK2VisitsRow:
    date = field(default='')
    sess_count = field(default='')


@define
class TelecomkzLK2UsersRow:
    date = field(default='')
    user_count = field(default='')


@define
class TelecomkzLK2Yam2VisitsRow:
    date = field(default='')
    sess_count = field(default='')


@define
class TelecomkzLK2Yam2UsersRow:
    date = field(default='')
    user_count = field(default='')


@define
class TelecomkzConversionsMainRow:
    conversion_id = field(default='')
    conversion_title = field(default='')
    date = field(default='')
    conversion_rate = field(default='')
    reaches = field(default='')
    visits = field(default='')
    converted_rub_revenue = field(default='')
    users = field(default='')
    page_views = field(default='')
    percent_new_visitors = field(default='')
    bounce_rate = field(default='')
    page_depth = field(default='')
    avg_visit_duration_seconds = field(default='')
    visits1 = field(default='')


@define
class TelecomkzConversionsLK1Row:
    conversion_id = field(default='')
    conversion_title = field(default='')
    date = field(default='')
    conversion_rate = field(default='')
    reaches = field(default='')
    visits = field(default='')
    converted_rub_revenue = field(default='')
    users = field(default='')
    page_views = field(default='')
    percent_new_visitors = field(default='')
    bounce_rate = field(default='')
    page_depth = field(default='')
    avg_visit_duration_seconds = field(default='')
    visits1 = field(default='')


@define
class TelecomkzConversionsLK2Row:
    conversion_id = field(default='')
    conversion_title = field(default='')
    date = field(default='')
    conversion_rate = field(default='')
    reaches = field(default='')
    visits = field(default='')
    converted_rub_revenue = field(default='')
    users = field(default='')
    page_views = field(default='')
    percent_new_visitors = field(default='')
    bounce_rate = field(default='')
    page_depth = field(default='')
    avg_visit_duration_seconds = field(default='')
    visits1 = field(default='')


@define
class TelecomkzLogsRow:
    visit_id = field(default='')
    counter_id = field(default='')
    watch_ids = field(default='')
    date = field(default='')
    date_time = field(default='')
    is_new_user = field(default='')
    page_views = field(default='')
    visit_duration = field(default='')
    bounce = field(default='')
    client_id = field(default='')
    counter_user_id_hash = field(default='')
    goals_id = field(default='')
    goals_date_time = field(default='')
    refere = field(default='')


@define
class TelecomkzRedesignLogsRow:
    visit_id = field(default='')
    counter_id = field(default='')
    watch_ids = field(default='')
    date = field(default='')
    date_time = field(default='')
    is_new_user = field(default='')
    page_views = field(default='')
    visit_duration = field(default='')
    bounce = field(default='')
    client_id = field(default='')
    counter_user_id_hash = field(default='')
    goals_id = field(default='')
    goals_date_time = field(default='')
    referer = field(default='')
    browser_language = field(default='')
    operating_system = field(default='')
    mobile_phone = field(default='')
    mobile_phone_model = field(default='')


@define
class TelecomkzWfmLogsRow:
    visit_id = field(default='')
    counter_id = field(default='')
    watch_ids = field(default='')
    date = field(default='')
    date_time = field(default='')
    is_new_user = field(default='')
    page_views = field(default='')
    visit_duration = field(default='')
    bounce = field(default='')
    client_id = field(default='')
    counter_user_id_hash = field(default='')
    goals_id = field(default='')
    goals_date_time = field(default='')
    referer = field(default='')
