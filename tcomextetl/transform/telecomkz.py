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
