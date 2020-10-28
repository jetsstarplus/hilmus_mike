from django.contrib import admin

from .models import Music

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

# Register your models here.
