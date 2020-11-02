from django.db import models

#this is for the news-letter subscribers
class Subscribers(models.Model):
    email = models.EmailField(unique=True)
    date_sent = models.DateTimeField(auto_now_add=True)
    is_checked = False
    
    def __str__(self):
        return self.email


#this is for the contacts
class Contact(models.Model):
    full_name = models.CharField(max_length=30)
    email = models.EmailField()
    subject = models.CharField(max_length = 80)
    content = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    is_checked = False
    is_confirmed = False
    
    def __str__(self):
        return self.full_name
# Create your models here.
