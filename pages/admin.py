from django.contrib import admin

from .models import Subscribers, Contact

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "date_sent", "is_checked")
    search_fields = ["email"]
    list_filter = ("email", "date_sent")
    actions = ['to_checked']
    
    def to_checked(self, queryset, request, *args, **kwargs):
        rows_updated = queryset.update(is_checked = True)
        
        if rows_updated == 1:
            message_bit = "1 subscription was"
        else:
            message_bit = "%s subscriptions were  " % self.rows_updated
            
        self.message_user(request, "%s successfully marked as checked " % message_bit)
        
    to_checked.short_description = "Change state Checked"
    
    
admin.site.register(Subscribers, SubscriberAdmin)
# Register your models here.

admin.site.register(Contact)

# Register your models here.
