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
