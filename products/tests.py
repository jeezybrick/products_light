# Create your tests here.

from django.test import Client, TestCase
from .models import MyUser, Item
from django.core.urlresolvers import reverse


class SimpleTest(TestCase):

    def setUp(self):
        # User objects
        self.user1 = MyUser.objects.create_user(
            'temporary', 'temporary@gmail.com', 'temporary', is_shop=False)
        self.user2 = MyUser.objects.create_user(
            'temporary2', 'temporary_second@gmail.com', 'temporary', is_shop=False)
        # Shop-user
        self.user_shop = MyUser.objects.create_user(
            'temporary3', 'temporary_shop@gmail.com', 'temporary', is_shop=True)
        # Item object
        self.item = Item(name='Phone 8080', price='1234', image_url='http://127.0.0.1:8000/products_ang/',
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
                         quantity=4, user=self.user1)
        self.item.save()
        # non exists item id
        self.fake_item_id = 9999
        self.client = Client()

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.user_shop.delete()
        self.item.delete()

    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_login_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_post(self):
        response = self.client.post(
            reverse('login'), {'username': 'john', 'password': 'smith'})
        self.assertEqual(response.status_code, 200)

    def test_register_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_post(self):
        response = self.client.post(
            reverse('register'), {'username': 'john', 'password': 'smith'})
        self.assertEqual(response.status_code, 200)

    """ Detail of item """
    def test_item_detail(self):
        response = self.client.get(
            reverse('products_show', args=(self.item.id, )))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse('products_show', args=(self.fake_item_id, )))
        self.assertEqual(response.status_code, 404)

    """
    test adding item
    Item can add only shop-users
    """
    def test_item_add(self):

        response = self.client.get(reverse('products_add'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse('products_add'))
        self.assertEqual(response.status_code, 403)

        response = self.client.post(reverse('products_add'), {
                                    'username': 'john', 'password': 'smith'})
        self.assertEqual(response.status_code, 403)

        self.client.login(username='temporary3', password='temporary')
        response = self.client.get(reverse('products_add'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('products_add'), {
                                    'username': 'john', 'password': 'smith'})
        self.assertEqual(response.status_code, 200)
