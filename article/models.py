import re

from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.sitemaps import ping_google
from django.utils.html import strip_tags

from django_summernote.fields import SummernoteTextFormField, SummernoteTextField

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Post(models.Model):
    image = models.ImageField(upload_to="Articles", null=True, blank=True, verbose_name="Title Image")
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(default=slugify(title),max_length=200, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    brief_information=models.TextField(verbose_name="Write a brief post info here", null=True, blank=True)
    content = SummernoteTextField(verbose_name="Write Your Post Here")
    read_time = models.IntegerField(verbose_name="Read Time", blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    
    def calculate_read_time(self, content_field):
        '''This method calculates the amount of time to read a blog'''
        content= strip_tags(content_field).strip()
        number = re.split(r'/W', content).count()
        read_time = round((number/100), 0)
        if read_time > 1:
            return read_time
        else:
            return 1
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.read_time=self.calculate_read_time(self.content)
        try:
            ping_google(sitemap_url='/sitemap.xml')
        except Exception:
            # Bare 'except' because we could get a variety
            # of HTTP-related exceptions.
            pass
        return super(Post, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("pages:article_detail", kwargs={"slug": str(self.slug)})
    
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)