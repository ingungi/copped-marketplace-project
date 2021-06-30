from django.test import TestCase
from authentication.views import dashboard_view,home_view
from django.urls import reverse,resolve

class testURL(TestCase):
    def test_home_url(self):
        url = reverse('Home')
        print(resolve(url))
    #testing if the url is correct
        self.assertEquals(resolve(url).func,home_view)
    def test_dashboard_url(self):
        url = reverse('dashboard')
        #testing if the url is wrong
        print(resolve(url))
        self.assertEquals(resolve(url).func,dashboard_view)




