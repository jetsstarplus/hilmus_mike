from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import Account


class AccountAdmin(UserAdmin):
    list_display = ('first_name', 'last_name','username','email', 'date_joined', 'avatar')
    list_display_links=('first_name', 'username', 'email')
   
    def profile(self, obj):
        return mark_safe('<img src = "{url}" width = "60px" height = "50px"/>'.format(
            url = obj.avatar.url,
             )
        )

    profile.short_description = 'Avatar'
   
admin.site.register(Account, AccountAdmin)
admin.site.empty_value_display = 'None'
# Register your models here.
