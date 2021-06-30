from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home_view, name='Home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.do_login, name='login'),
    path('logout/', views.do_logout, name='logout'),
    path('dashboard/listing/', views.posting, name='add_listing'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('change_password/', views.change_password, name='change_password'),
    path('chat/', include('messaging.urls'), name='chatbox'),
    path('charge/', views.charge, name='charge'), # new
    path('payment/', views.HomePageView.as_view(), name='payment'),
    path('cart_view/', views.cart_view, name='cart_view'),
    path('past_orders/', views.past_orders, name='past_orders'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




