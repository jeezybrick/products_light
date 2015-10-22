# Create your tests here.

from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from products import models
from cart.models import Cart
from my_auth.models import MyUser


class SimpleTest(TestCase):
    def setUp(self):
        # User objects
        self.user1 = MyUser.objects.create_user('temporary', 'temporary@gmail.com',
                                                'temporary', is_shop=False)
        self.user2 = MyUser.objects.create_user('temporary2', 'temporary_second@gmail.com',
                                                'temporary', is_shop=False)
        # Shop-user
        self.user_shop = MyUser.objects.create_user('temporary3', 'temporary_shop@gmail.com',
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

        self.client = Client()

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.user_shop.delete()
        self.item.delete()

    """ List of items """

    def test_item_list(self):
        url = reverse('item_list_api')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    """ Detail of item """

    def test_item_detail(self):
        url = reverse('item_detail_api', args=(self.item.id,))
        url_with_fake_id = reverse('item_detail_api', args=(self.fake_id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(url_with_fake_id)
        self.assertEqual(response.status_code, 404)

    """ test add item """

    def test_item_add(self):
        url = reverse('item_list_api')
        post = {'username': 'john', 'password': 'smith'}
        response = self.client.post(url, post)

        # no post method allowed
        self.assertEqual(response.status_code, 405)

    """ test edit item with permission to edit and delete only owner """

    def test_item_edit(self):
        url = reverse('item_detail_api', args=(self.item.id,))
        post = {'name': 'john', 'price': 322}

        # PUT and DELETE without auth
        response = self.client.put(url, post)
        self.assertEqual(response.status_code, 403)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

        # PUT and DELETE by no owner of item
        self.client.login(username='temporary', password='temporary')
        response = self.client.put(url, post)
        self.assertEqual(response.status_code, 403)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

        # PUT and DELETE by owner
        self.client.login(username='temporary3', password='temporary')
        response = self.client.put(url, post)
        self.assertEqual(response.status_code, 415)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    """ List of action """

    def test_action_list(self):
        url = reverse('action_list_api')

        # get by anonymous user
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # get by auth user
        self.client.login(username='temporary3', password='temporary')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    """
        test add action with permission to add and only shop-user
        and edit only by owner
    """

    def test_add_action(self):
        url = reverse('action_list_api')
        post = {'item': str(self.item.id), 'description': 'test desc',
                'new_price': 1224, 'period_from': "2015-10-05", 'period_to': "2015-10-12"}

        # get and post by anonymous user
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        response = self.client.post(url, post)
        self.assertEqual(response.status_code, 403)

        # get and post by auth user and owner
        self.client.login(username='temporary3', password='temporary')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url, post)
        self.assertEqual(response.status_code, 201)

        # post by auth user and NO owner of item
        self.client.login(username='temporary', password='temporary')
        response = self.client.post(url, post)
        self.assertEqual(response.status_code, 403)

    """ Delete action """
    def test_delete_action(self):
        url_list = reverse('action_list_api')
        url_detail = reverse('action_detail_api', args=(self.item.id,))
        post = {'item': str(self.item.id), 'description': 'test desc',
                'new_price': 1224, 'period_from': "2015-10-05", 'period_to': "2015-10-12"}

        # create action by auth user
        self.client.login(username='temporary3', password='temporary')
        response = self.client.post(url_list, post)
        self.assertEqual(response.status_code, 201)

        # delete action by no owner
        self.client.login(username='temporary', password='temporary')
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, 404)

        # delete action by owner
        self.client.login(username='temporary3', password='temporary')
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, 204)

    """ Add category(no post method) """

    def test_add_category(self):
        url = reverse('category_list_api')
        post = {'username': 'john', 'password': 'smith'}
        response = self.client.post(url, post)

        # no post method allowed
        self.assertEqual(response.status_code, 405)

    """ Add comment by auth and no auth user """

    def test_add_comment(self):
        url = reverse('comment_list_api')
        post = {'username': 'john', 'message': 'smith', 'item': self.item.id}

        post_with_fake_id = {'username': 'john', 'message': 'smith', 'item': self.fake_id}
        response = self.client.post(url, post)
        self.assertEqual(response.status_code, 201)

        # bad POST
        response = self.client.post(url, post_with_fake_id)
        self.assertEqual(response.status_code, 400)

    """ Add rating to item by AUTH user """

    def test_add_rate(self):
        url = reverse('rate_list_api')
        post = {'value': 5, 'item': self.item.id}
        post_with_error = {'value': -2, 'item': self.fake_id}

        # 403 for no auth user
        response = self.client.post(url, post)
        self.assertEqual(response.status_code, 403)

        # 201 FOR AUTH USER
        self.client.login(username='temporary3', password='temporary')
        response = self.client.post(url, post)
        self.assertEqual(response.status_code, 201)

        # bad POST
        response = self.client.post(url, post_with_error)
        self.assertEqual(response.status_code, 400)

    """ Shop list """

    def test_shop_list(self):
        url = reverse('shop_list_api')
        post = {'test': 5}

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # post not allowed
        response = self.client.post(url, post)
        self.assertEqual(response.status_code, 405)

    """ Shop detail """

    def test_shop_detail(self):
        url = reverse('shop_detail_api', args=(self.user_shop.id,))
        post = {'test': 5}

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # post not allowed
        response = self.client.post(url, post)
        self.assertEqual(response.status_code, 405)

    """ List of item added by current auth user in the cart """

    def test_cart_list(self):
        url = reverse('cart_list_api')
        post = {'item': self.item.id}
        post_with_fake_id = {'item': self.fake_id}

        # get,post by anonymous user
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # post item in the cart by anonymous user
        response = self.client.post(url, post)
        self.assertEqual(response.status_code, 403)

        # get,post by auth user
        self.client.login(username='temporary3', password='temporary')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # post item in the cart
        response = self.client.post(url, post)
        self.assertEqual(response.status_code, 201)

        # bad request
        response = self.client.post(url, post_with_fake_id)
        self.assertEqual(response.status_code, 400)

    """ Detail of item in the cart """

    def test_cart_detail(self):
        url_detail = reverse('cart_detail_api', args=(self.item.id,))
        url_detail_with_fake_id = reverse('cart_detail_api', args=(self.fake_id,))
        url = reverse('cart_list')
        post = {'item': self.item.id}

        # create cart
        cart = Cart(user=self.user1, item=self.item)
        cart.save()

        # get,post by anonymous user
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, 403)

        # get,post by auth user
        self.client.login(username='temporary3', password='temporary')

        # Add item to the cart
        self.client.post(url, post)
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, 200)

        # Get to non exists cart detail
        response = self.client.get(url_detail_with_fake_id)
        self.assertEqual(response.status_code, 404)
