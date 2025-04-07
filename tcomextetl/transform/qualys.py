from attrs import define, field

@define
class QualysVulnerabilitiesRow:
    qid: str = field(default='')
    title: str = field(default='')
    severity: str = field(default='')
    last_detected: str = field(default='')
    first_detected: str = field(default='')
    status: str = field(default='')
    asset_name: str = field(default='')
    asset_ipv4: str = field(default='')
    asset_tags: str = field(default='')
    disabled: str = field(default='')
    ignored: str = field(default='')
    qds: str = field(default='')
    qds_severity: str = field(default='')
    true_risk_score: str = field(default='')