from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='chatbox'),
    path('<str:room_name>/', views.room, name='room'),
]