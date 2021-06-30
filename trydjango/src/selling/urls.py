from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('listing/', posting, name='add_listing')

]
