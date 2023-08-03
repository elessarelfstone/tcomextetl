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

