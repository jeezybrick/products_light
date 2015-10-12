"""add/remove item id to/from session 'in_cart'"""


def addItemIdToSession(request):

    if request.session.get('in_cart', False):
        request.session['in_cart'].append(request.data["item"])
        request.session.modified = True
    else:
        request.session['in_cart'] = [request.data["item"]]


def removeItemIdFromSession(request, item_id):
    if request.session.get('in_cart', False):
        request.session['in_cart'].remove(int(item_id))

    if not request.session.get('in_cart', False):
        del request.session['in_cart']

    request.session.modified = True
