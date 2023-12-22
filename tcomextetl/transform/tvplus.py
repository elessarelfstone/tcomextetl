from attrs import define, field


@define
class TvPlusCinemaStartRow:
    id = field(default='')
    title = field(default='')
    genre = field(default='')
    category = field(default='')
    agerating = field(default='')
    ratingimdb = field(default='')
    ratingkp = field(default='')
    description = field(default='')


@define
class TvPlusCinemaKazvodRow:
    id = field(default='')
    title = field(default='')
    genre = field(default='')
    category = field(default='')
    agerating = field(default='')
    ratingimdb = field(default='')
    ratingkp = field(default='')
    description = field(default='')


@define
class TvPlusCinemaMegogoRow:
    id = field(default='')
    title = field(default='')
    genre = field(default='')
    category = field(default='')
    agerating = field(default='')

@define
class TvPlusProgramsRow:
    channel_id = field(default='')
    program_id = field(default='')
    program = field(default='')
    description = field(default='')
    agerating = field(default='')
    start = field(default='')
    end = field(default='')
    duration = field(default='')
    update_info = field(default='')
