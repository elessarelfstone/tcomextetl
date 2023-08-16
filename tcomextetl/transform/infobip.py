from attrs import define, field


@define
class InfobipAgentRow:
    id = field(default='')
    displayname = field(default='')
    status = field(default='')
    availability = field(default='')
    role = field(default='')
    enabled = field(default='')
    createdat = field(default='')
    updatedat = field(default='')


@define
class InfobipQueueRow:
    id = field(default='')
    name = field(default='')
    createdat = field(default='')
    updatedat = field(default='')
    isautoassignmentenabled = field(default='')
    stickyagenttimeoutdays = field(default='')
    isstickyautoassignmentenabled = field(default='')
    workingHoursid = field(default='')
    deletedat = field(default='')


@define
class InfobipConversationRow:
    id = field(default='')
    topic = field(default='')
    summary = field(default='')
    status = field(default='')
    priority = field(default='')
    queueid = field(default='')
    agentid = field(default='')
    createdat = field(default='')
    updatedat = field(default='')
    closedat = field(default='')


@define
class InfobipConvMessagesRow:
    id = field(default='')
    channel = field(default='')
    from_ = field(default='')
    to = field(default='')
    direction = field(default='')
    conversationid = field(default='')
    createdat = field(default='')
    updatedat = field(default='')
    contenttype = field(default='')
    text = field(default='')


@define
class InfobipConvTagsRow:
    conversationid = field(default='')
    name = field(default='')
    createdat = field(default='')
    updatedat = field(default='')
