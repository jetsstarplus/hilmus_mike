from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Music, StaffMember, Testimonial, TermsOfService

class MusicAdmin(admin.ModelAdmin):
    list_display= ('artist', 'title', 'music', 'is_sent')
    list_filter=('artist', 'title', 'is_sent')
    ordering=('-date_added', 'is_sent')
    
    def make_sent(self, request, queryset):
       rows_updated= queryset.update(is_sent=True)
       if rows_updated == 1:
           message_bit = "1 music was"
       else:
           message_bit = "{} musics were ".format(rows_updated)
           
       self.message_user(request, "{} successfully marked as sent".format(message_bit))
    
    make_sent.short_description= "Mark Selected Musics To Sent"
    make_sent.allowed_permissions = ('change', )

admin.site.register(Music, MusicAdmin)

class StaffAdmin(admin.ModelAdmin):
    """A staffs Admin class"""
    list_display = ('name', 'role', 'rank', 'is_published')
    list_filter=('name', 'role', 'rank', 'is_published')
    ordering=('-rank', 'is_published')
    search_fields=['name', 'role']

admin.site.register(StaffMember, StaffAdmin)

class TestimonialAdmin(admin.ModelAdmin):
    """A testimonial Admin Class"""
    list_display= ('name', 'content', 'is_published')
    list_filter=('name', 'is_published')
    ordering=('-date_added', 'is_published')
    search_fields=['name', 'content']
    
admin.site.register(Testimonial, TestimonialAdmin)

class TermsAdmin(SummernoteModelAdmin):
    """A terms of service admin model"""
    list_display=('title', 'content')
    summernote_fields=('content')
    # search_fields=('title', 'content')
    
admin.site.register(TermsOfService, TermsAdmin)
# Register your models here.
