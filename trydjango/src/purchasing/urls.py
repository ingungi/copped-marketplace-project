from django.urls import path, include

from . import views
from .views import (OrderSummaryView)

urlpatterns = [
	path('menswear', views.menswear, name='menswear'),
	path('womenswear', views.womenswear, name='womenswear'),
	path('accessories', views.accessories, name='accessories'),
	path('footwear', views.footwear, name='footwear'),
	path('product/<int:Item>/', views.product, name='product'),
	path('designer/<str:Brand>/', views.designer, name='designer'),
	path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
	path('designers/', views.designer_home, name='designer_home'),
	path('add-to-cart/<int:id>/', views.add_to_cart, name='add-to-cart'),
	path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove-from-cart'),
	path('checkout/', views.checkout, name='checkout'),
	path('change_listing/<int:item_id>/', views.change_listing, name='change_listing'),
	path('delete/<int:item_id>/', views.delete_listing, name='delete_listing')
 ]
