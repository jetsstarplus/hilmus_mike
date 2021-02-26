from django.db import models
from django.conf import settings
from datetime import datetime
from django.utils import timezone
import uuid
from django.template.defaultfilters import slugify
from django.contrib.sitemaps import ping_google

from .upload_handler import validate_file_extension
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField
# from account.models import SeoModel

class Music(models.Model):
    """A model that represents a particular Music uploaded by an artist, This particular music is checked whether
     it has already been sent to boomplay or skiza
    """
    # id=models.UUIDField(primary_key=True, default=uuid.uuids4, editable=False)
    artist=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=False, blank=True, related_name="musics")
    description= models.TextField(blank=True, null=True, verbose_name="More Information",)
    title= models.CharField(blank=True, max_length=50, null=True)
    music=models.FileField(upload_to="Musics", validators=[validate_file_extension], verbose_name="Audio File")
    picture=models.ImageField(upload_to="Music-pics", null=True, blank=True)
    is_sent=models.BooleanField(default=False, verbose_name="Has been sent")
    is_boompay=models.BooleanField(default=True, verbose_name="To upload to boomplay")
    is_skiza=models.BooleanField(default=False, verbose_name="Generate the skiza code", null=True, blank=True)  
    skiza_code= models.CharField(max_length=50, blank=True, null=True, verbose_name="The generated Skiza Code")  
    seo_title=models.CharField(max_length=50, blank=True, null=True)
    seo_description=models.TextField(blank=True, null=True) 
    date_added= models.DateTimeField(auto_now_add=True)
    date_updated= models.DateTimeField(auto_now=True)
    
    
    def updated_recently(self):
        pass
    
    def __str__(self):
        return(self.music, " by ", self.artist)
    
class Testimonial(models.Model):
    """A model for creating a testimonial person/ member"""
    name=models.CharField(max_length=30)
    picture=models.ImageField(upload_to="testimonials", blank=True, null=True)
    is_published= models.BooleanField(default=False, verbose_name="Publish Testimonial?")
    content= models.TextField()
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
    date_added= models.DateTimeField(auto_now_add=True)
    date_updated= models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return(self.name)
    
class StaffMember(models.Model):
    """A model for creating a testimonial person/ member"""
    username= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Username Of the staff Member")
    role=models.CharField(max_length=35)
    rank= models.IntegerField(default=1)
    picture=models.ImageField(upload_to="testimonials", blank=True, null=True)
    is_published= models.BooleanField(default=False, verbose_name="Publish Testimonial?")
    facebook= models.CharField(max_length=50, blank=True, null=True, verbose_name="Facebook Link")
    twitter=models.CharField(max_length=50, blank=True, null=True, verbose_name="Twitter Link")
    instagram=models.CharField(max_length=50, blank=True, null=True, verbose_name="Instagram Link")
    
    def __str__(self):
        return(self.name)
    

class TermsOfService(models.Model):
    """A model representing the terms of service contents"""
    title= models.CharField(max_length=30)
    content= SummernoteTextField()
    date_added=models.DateTimeField(auto_now_add=True)
    date_modified= models.DateTimeField(auto_now=True)
    
    def _str__(self):
        return(self.title)
    

class Service(models.Model):
    """ A model representing the services that are offered by mike creatives """
    title= models.CharField(max_length=30)
    slug=models.SlugField(unique=True, max_length=200, null=True, blank=True)
    image= models.ImageField(upload_to='services', blank=True, null=True)
    font_image= models.CharField(max_length=40)
    home_page_text= models.TextField()
    pricing= models.CharField(max_length=10)    
    content= SummernoteTextField()
    date_added=models.DateTimeField(auto_now_add=True)
    date_modified= models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering=['title']
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        try:
            ping_google(sitemap_url='/sitemap.xml')
        except Exception:
            # Bare 'except' because we could get a variety
            # of HTTP-related exceptions.
            pass
        return super(Service, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("pages:services", kwargs={"slug": str(self.slug)})
    
# Create your models here.
class CategoryItem(models.Model):
    """This is the category items"""
    title=models.TextField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="category the item belongs to")
    Image = models.ImageField(upload_to="categoryItemImages", blank=True, null=True, verbose_name='Item Image')
    PDF = models.FileField(upload_to='categoryItemPdf', blank=True, null=False, verbose_name="Category Item Pdf")
    content=SummernoteTextField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True)
