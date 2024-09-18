from attrs import define, field


@define
class ShopTelecomKzNursatPlusRow:
    id = field(default='')
    kt_managers = field(default='')
    contract = field(default='')
    status = field(default='')
    sum = field(default='')
    created_at = field(default='')
    product_name = field(default='')
    quantity = field(default='')