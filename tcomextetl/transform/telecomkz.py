from attrs import define, field


@define
class TelecomkzMainVisitsRow:
    date = field(default='')
    users_count = field(default='')


@define
class TelecomkzMainUsersRow:
    date = field(default='')
    users_count = field(default='')


@define
class TelecomkzLK1VisitsRow:
    date = field(default='')
    users_count = field(default='')


@define
class TelecomkzLK1UsersRow:
    date = field(default='')
    users_count = field(default='')


@define
class TelecomkzLK2VisitsRow:
    date = field(default='')
    users_count = field(default='')


@define
class TelecomkzLK2UsersRow:
    date = field(default='')
    users_count = field(default='')


@define
class TelecomkzLK2Yam2VisitsRow:
    date = field(default='')
    users_count = field(default='')


@define
class TelecomkzLK2Yam2UsersRow:
    date = field(default='')
    users_count = field(default='')
