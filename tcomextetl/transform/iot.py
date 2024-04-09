from attrs import define, field


@define
class IotStatRow:
    tech_service_code = field(default='')
    tech_service_count = field(default='')
    town_id = field(default='')
    product_id = field(default='')
    customer_account_id = field(default='')
    event_date = field(default='')
    product_num = field(default='')
    product_offer_struct_id = field(default='')
    filial_id = field(default='')
    total_nodes = field(default='')
    total_msg = field(default='')
