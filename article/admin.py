from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin

from .models import Post, Comment


class CommentInline(admin.TabularInline):
    model=Comment
    extra=0

# Register your models here.
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug','status','author', 'updated_on')
    list_display_links=('title', 'slug', 'author')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    summernote_fields=('content',)
    prepopulated_fields = {'slug': ('title',)}
    inlines= [
        CommentInline,
    ]
    
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

admin.site.register(Comment, CommentAdmin)   
        
admin.site.empty_value_display = 'None'