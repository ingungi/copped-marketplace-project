from django.db import models

class Messages(models.Model):

    message = models.TextField(max_length=10000)
    sender = models.CharField(max_length=120)
    created = models.DateTimeField(auto_now_add=True)

    #def __str__(self):
     #   return self.message
# Create your models here.
