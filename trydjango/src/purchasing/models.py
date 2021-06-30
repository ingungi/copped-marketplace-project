from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from selling.models import Item_posting
# Create your models here.

class CartItem(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
	item = models.OneToOneField(Item_posting, on_delete=models.SET_NULL, null=True)
	ordered = models.BooleanField(default=False)
	quantity = models.IntegerField(default=1)

#	def __str__(self):
#		return {str(self.item.item.all()[0].title)}

	def get_total_item_price(self):
		return self.quantity * self.item.price

	def get_final_price(self):
		 return self.get_total_item_price()


class Cart(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
	order_date = models.DateField(null=True)
	payment_id = models.CharField(max_length=100, null=True)
	name = models.CharField(max_length=100, null=True)
	city = models.CharField(max_length=100, null=True)
	province = models.CharField(max_length=15, null=True)
	postal_code = models.CharField(max_length=100, null=True)
	items = models.ManyToManyField(CartItem)
	active = models.BooleanField(default=True)
	purchased = models.BooleanField(default=False)
	address = models.CharField(max_length=100, null=True)

	def __str__(self):
		 return str(self.user.username)

	def get_total(self):
		total = 0
		for cartitem in self.items.all():
			total += cartitem.get_final_price()
		return total
	def get_total_shipping(self):
		total = 30
		for cartitem in self.items.all():
			total += cartitem.get_final_price()
		return total