from django.test import TestCase, Client
from django.urls import reverse
from selling.models import Item_posting
from purchasing.models import Cart, CartItem
import json
from django.contrib.auth.models import User

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        user= User.objects.create_user(username='john',
                                 email='jlennon@beatles.com',
                                 password='glass onion')
        self.p=Item_posting.objects.create(owner=user,title='h',image='static/images/home_image.jpeg',descrip='h',
                            quantity=2,
                            image2='static/images/home_image.jpeg',
                            image3='static/images/home_image.jpeg',
                            image4='static/images/home_image.jpeg',
                            designer='h',
                            price=2,
                            color='h',
                            type='1'
        )

    def test_product_view(self):
        #testing if the product view renders right one
        response = self.client.get(reverse('product', args=[self.p.id]))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'clothing/product.html')

    def test_delete(self):
        user = User.objects.create_user(username='johnny',
                                        email='jlennon@beatles.com',
                                        password='glass onion')
        p = Item_posting.objects.create(owner=user, title='h', image='static/images/home_image.jpeg', descrip='h',
                                        quantity=2,
                                        image2='static/images/home_image.jpeg',
                                        image3='static/images/home_image.jpeg',
                                        image4='static/images/home_image.jpeg',
                                        designer='h',
                                        price=2,
                                        color='h',
                                        type='1'
                                        )
        response = self.client.get(reverse('delete_listing',args=[p.id]))
        self.assertEquals(response.status_code,302)


