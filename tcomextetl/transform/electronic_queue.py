from attrs import define, field


@define
class ElectronicQueueRow:
    serviceoffice = field(default='')
    receptionwindow = field(default='')
    day = field(default='')
    ticketnumber = field(default='')
    visitorarrivaldatetime = field(default='')
    starttime = field(default='')
    endtime = field(default='')
    personalid = field(default='')
    service = field(default='')
    result = field(default='')
    iseligibleforbenefits = field(default='')
    language = field(default='')
    reservationnumber = field(default='')
    pssid = field(default='')
    ldaplogin = field(default='')