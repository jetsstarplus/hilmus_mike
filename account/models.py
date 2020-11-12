from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from daraja.models import Lipa_na_mpesa
from mike_admin.models import Service

# from phonenumbers import 

# from versatileimagefield.fields import VersatileImageField
# from versatileimagefield.placeholder import OnStoragePlaceholderImage
# Create your models here.

class Account(AbstractUser):
    avatar = models.ImageField(
        upload_to="avatars", verbose_name='avatar', null=True, 
        blank=True)
    is_payed = models.BooleanField(default=False, null=False, blank=False)
    tos=models.BooleanField(null=True, blank=True, default=False)
    transaction_id = models.TextField(null=True, blank=True)
    information= models.TextField(null=True, blank=True, verbose_name="About Yourself")
    phone=models.TextField(null=True, blank=True, verbose_name='phone number')
    
    # @receiver(models.signals.post_delete, sender=avatar)
    # def delete_ExampleImageModel_images(sender, instance, **kwargs):
    #     """
    #     Deletes ExampleImageModel image renditions on post_delete.
    #     """
    #     # Deletes Image Renditions
    #     instance.image.delete_all_created_images()
    #     # Deletes Original Image
    #     instance.image.delete(save=False)
# class SeoModel(models.Model):
class UserPayment(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    transaction_id= models.CharField(max_length=20)
    service= models.ForeignKey(Service, on_delete=models.PROTECT)
    date_submitted=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return("{} - {} for {}".format(self.user, self.transaction_id, self.service))
    