from typing import assert_never


def get_head(obj: dict, list_or_item_key: str, item_attribute_name: str = "value", default=None):
    list_or_item = obj.get(list_or_item_key)
    if not list_or_item:
        return default

    if isinstance(list_or_item, list):
        item = list_or_item[0]
    elif isinstance(list_or_item, dict):
        item = list_or_item
    else:
        return list_or_item

    if not item_attribute_name:
        return item
    return item.get(item_attribute_name, default)


def ean2gtin(code: str) -> str:
    """
    Convert EAN-13 and EAN-8 code to GTIN code.
    """
    if len(code) == 13:
        return f"0{code}"

    elif len(code) == 8:
        return f"000000{code}"

    else:
        assert_never(code)
