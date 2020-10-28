from django.db import models
from django.conf import settings
from datetime import datetime, timezone
import uuid

# from account.models import SeoModel

class Music(models.Model):
    """A model that represents a particular Music uploaded by an artist, This particular music is checked whether
     it has already been sent to boomplay or skiza
    """
    id=models.UUIDField(primary_key=True, default=uuid.uuid4())
    artist=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=False, blank=True)
    description= models.TextField(blank=True, null=True, verbose_name="More Information")
    title= models.CharField(blank=False, max_length=30)
    music=models.FileField(upload_to="Musics")
    picture=models.ImageField(upload_to="Music-pics")
    is_sent=models.BooleanField(default=False, verbose_name="Has been sent")
    is_boompay=models.BooleanField(default=True, verbose_name="To upload to boomplay")
    is_skiza=models.BooleanField(default=False, verbose_name="Generate the skiza code", null=True, blank=True)    
    seo_title=models.CharField(max_length=50, blank=True, null=True)
    seo_description=models.TextField(blank=True, null=True) 
    date_added= models.DateTimeField(auto_now_add=True)
    date_updated= models.DateTimeField(auto_now=True)
    
    def updated_recently(self):
        pass
    
    def __repr__(self):
        return(self.music, " by ", self.artist)
    
# Create your models here.
