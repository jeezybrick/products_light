
from .models import Category

""" parent category choices """


def categories_as_choices():
    return [[category.id, category.name] for category in Category.objects.filter(parent_category_id__isnull=True)]


""" return message depends on quantity item """


def message_of_quantity_items(item):
    try:
        item.quantity
    except:
        return None
    else:
        if item.quantity == 0:
            return 'The product is out of stock'
        if item.quantity < 10:
            return 'The product ends'


""" return item with percentage price """


def price_with_percent(item):
    if item.user.percentage_of_price:
        item.price = item.price * item.user.percentage_of_price / 100
    return item
