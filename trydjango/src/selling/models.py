from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
# Create your models here.
def get_upload_path(instance, filename):
	return 'user-'+str(instance.owner.id)+'/'+filename

class Item_posting(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=25, null=True)
	size = models.CharField(max_length=4, null=True)
	image = models.FileField()
	image2 = models.FileField(blank = True)
	image3 = models.FileField(blank = True)
	image4 = models.FileField(blank = True)
	descrip = models.CharField(max_length=10000)
	quantity = models.IntegerField(blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	designer = models.CharField(max_length=50, blank = False)
	price = models.DecimalField(decimal_places=2,max_digits=1000)
	color = models.CharField(max_length=50)
	SUB_CHOICES=(
		('1',"Womenswear"),
		('2', "Menswear"),
		('3', "Accesories"),
		('4', "Footwear"),
	)
	type = models.CharField(max_length=1, choices=SUB_CHOICES)

	def __str__(self):
		return self.title

	def get_add_to_cart_url(self):
		return reverse("add-to-cart", kwargs={'id': self.id})
   
	def get_remove_from_cart_url(self):
		return reverse("remove-from-cart", kwargs={'id': self.id})
