
""" return message depends on quantity item """


def message_of_quantity_items(item):
    if item.quantity is not None:
        if item.quantity == 0:
            return 'The item is out of stock :('
        if item.quantity < 10:
            return 'This item end soon! Hurry up!'
    return None


""" return item with percentage price """


def price_with_percent(item):
    if item.user.percentage_of_price:
        item.price = item.price * item.user.percentage_of_price / 100
    return item
