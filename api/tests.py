# Create your tests here.

import datetime
from django.test import Client, TestCase
from products import models
from django.core.urlresolvers import reverse


class SimpleTest(TestCase):
    def setUp(self):
        # User objects
        self.user1 = models.MyUser.objects.create_user('temporary', 'temporary@gmail.com',
                                                       'temporary', is_shop=False)
        self.user2 = models.MyUser.objects.create_user('temporary2', 'temporary_second@gmail.com',
                                                       'temporary', is_shop=False)
        # Shop-user
        self.user_shop = models.MyUser.objects.create_user('temporary3', 'temporary_shop@gmail.com',
                                                           'temporary', is_shop=True)
        # Create Item object
        self.item = models.Item(name='Phone 8080', price='1234', image_url='http://127.0.0.1:8000/products_ang/',
                                description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam elementum'
                                            ' hendrerit ullamcorper. Nam ultrices sapien sit amet velit feugiat condimentum '
                                            'at in arcu. Donec ac ligula accumsan, consequat ligula a, ultrices ligula. '
                                            'Vivamus rutrum, eros a elementum ultrices, leo ipsum sollicitudin metus, nec '
                                            'aliquet leo magna nec orci. Nulla neque dui, suscipit ac consequat ac, rutrum nec '
                                            'sem. Duis quis velit id justo accumsan suscipit sit amet vel sem. Sed at porttitor '
                                            'odio, vel feugiat lectus. Integer et ex vitae elit hendrerit aliquet. Pellentesque'
                                            ' pulvinar, justo quis tristique dignissim, ex lorem convallis erat, at consectetur'
                                            ' mi justo at arcu. Ut tristique facilisis magna interdum malesuada. Interdum et malesuada '
                                            'fames ac ante ipsum primis in faucibus. Duis sed commodo arcu. Nullam a orci imperdiet, '
                                            'pulvinar orci id, pretium augue.',
                                quantity=4, user=self.user_shop)
        self.item.save()
        # non exists item id
        self.fake_id = 9999
        # add action dict
        self.action_values = {'item': self.item, 'shop': self.user_shop, 'description': 'test desc', 'new_price': 1224,
                              'period_from': datetime.date.today, 'period_to': datetime.date.today}
        self.client = Client()

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.user_shop.delete()
        self.item.delete()

    """ List of items """

    def test_item_list(self):
        response = self.client.get(reverse('item-list'))
        self.assertEqual(response.status_code, 200)

    """ Detail of item """

    def test_item_detail(self):
        response = self.client.get(
            reverse('item-detail', args=(self.item.id,)))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse('item-detail', args=(self.fake_id,)))
        self.assertEqual(response.status_code, 404)

    """ test add item """

    def test_item_add(self):
        response = self.client.post(
            reverse('item-list'), {'username': 'john', 'password': 'smith'})
        # no post method
        self.assertEqual(response.status_code, 405)

    """ test edit item with permission to edit and delete only owner """

    def test_item_edit(self):
        # PUT and DELETE without auth
        response = self.client.put(reverse('item-detail', args=(self.item.id,)),
                                   {'name': 'john', 'price': 322})
        self.assertEqual(response.status_code, 403)

        response = self.client.delete(
            reverse('item-detail', args=(self.item.id,)))
        self.assertEqual(response.status_code, 403)

        # PUT and DELETE by no owner of item
        self.client.login(username='temporary', password='temporary')
        response = self.client.put(reverse('item-detail', args=(self.item.id,)),
                                   {'name': 'john', 'price': 322})
        self.assertEqual(response.status_code, 403)

        response = self.client.delete(
            reverse('item-detail', args=(self.item.id,)))
        self.assertEqual(response.status_code, 403)

        # PUT and DELETE by owner
        self.client.login(username='temporary3', password='temporary')
        response = self.client.put(reverse('item-detail', args=(self.item.id,)),
                                   {'name': 'john', 'price': 322})
        self.assertEqual(response.status_code, 415)

        response = self.client.delete(
            reverse('item-detail', args=(self.item.id,)))
        self.assertEqual(response.status_code, 204)

    """ List of action """

    def test_action_list(self):
        # get by anonymous user
        response = self.client.get(reverse('action-list'))
        self.assertEqual(response.status_code, 200)

        # get by auth user
        response = self.client.get(reverse('action-list'))
        self.assertEqual(response.status_code, 200)

    """
        test add action with permission to add and only shop-user
        and edit only by owner
    """

    def test_add_action(self):
        response = self.client.post(reverse('action-list'), self.action_values)
        self.assertEqual(response.status_code, 200)

    """ Add category(no post method) """

    def test_add_category(self):
        response = self.client.post(
            reverse('category-list'), {'username': 'john', 'password': 'smith'})
        # no post method
        self.assertEqual(response.status_code, 405)

    """ Add comment by auth and no auth user """

    def test_add_comment(self):
        response = self.client.post(reverse('comment-list'), {'username': 'john', 'message': 'smith',
                                                              'item': self.item.id})
        self.assertEqual(response.status_code, 201)

        # bad POST
        response = self.client.post(reverse('comment-list'), {'username': 'john', 'message': 'smith',
                                                              'item': self.fake_id})
        self.assertEqual(response.status_code, 400)

    """ Add rating to item by AUTH user """

    def test_add_rate(self):
        # 403 for no auth user
        response = self.client.post(
            reverse('rate-list'), {'value': 5, 'item': self.item.id})
        self.assertEqual(response.status_code, 403)

        # 201 FOR AUTH USER
        self.client.login(username='temporary3', password='temporary')
        response = self.client.post(
            reverse('rate-list'), {'value': 5, 'item': self.item.id})
        self.assertEqual(response.status_code, 201)

        # bad POST
        response = self.client.post(
            reverse('rate-list'), {'value': -2, 'item': self.fake_id})
        self.assertEqual(response.status_code, 400)

    """ Shop list """

    def test_shop_list(self):
        response = self.client.get(reverse('shop-list'))
        self.assertEqual(response.status_code, 200)

        # post not allowed
        response = self.client.post(reverse('shop-list'), {'test': 5})
        self.assertEqual(response.status_code, 405)

    """ Shop detail """

    def test_shop_detail(self):
        response = self.client.get(
            reverse('shop-detail', args=(self.user_shop.id,)))
        self.assertEqual(response.status_code, 200)

        # post not allowed
        response = self.client.post(
            reverse('shop-detail', args=(self.user_shop.id,)), {'test': 5})
        self.assertEqual(response.status_code, 405)

    """ List of item added by current auth user in the cart """

    def test_cart_list(self):
        # get,post by anonymous user
        response = self.client.get(reverse('cart-list'))
        self.assertEqual(response.status_code, 403)

        # post item in the cart
        response = self.client.post(reverse('cart-list'), {'item': self.item})
        self.assertEqual(response.status_code, 403)

        # get,post by auth user
        self.client.login(username='temporary3', password='temporary')
        response = self.client.get(reverse('cart-list'))
        self.assertEqual(response.status_code, 200)

        # post item in the cart
        response = self.client.post(
            reverse('cart-list'), {'item': self.item.id})
        self.assertEqual(response.status_code, 201)

        # bad request
        response = self.client.post(
            reverse('cart-list'), {'item': self.fake_id})
        self.assertEqual(response.status_code, 400)

    """ Detail of item in the cart """

    def test_cart_detail(self):
        # create cart
        cart = models.Cart(user=self.user1, item=self.item)
        cart.save()

        # get,post by anonymous user
        response = self.client.get(
            reverse('cart-detail', args=(self.item.id,)))
        self.assertEqual(response.status_code, 403)

        # get,post by auth user
        self.client.login(username='temporary3', password='temporary')

        # Add item to the cart
        self.client.post(reverse('cart-list'), {'item': self.item.id})
        response = self.client.get(
            reverse('cart-detail', args=(self.item.id,)))
        self.assertEqual(response.status_code, 200)

        # Get to non exists cart detail
        response = self.client.get(
            reverse('cart-detail', args=(self.fake_id,)))
        self.assertEqual(response.status_code, 404)
