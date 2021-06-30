from django.test import TestCase, Client
from django.urls import reverse
from purchasing.models import *
from selling.models import *
import json

class TestViews(TestCase):
    def setup(self):
        self.client = Client()
        self.url = reverse('designer')
    def checkdesigner(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'womenOrMen.html')