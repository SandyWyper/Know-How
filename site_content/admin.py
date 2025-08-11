from django.contrib import admin

# Register your models here.
from .models import Page, NavigationList
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on', 'updated_on')
    search_fields = ['title']
    list_filter = ('status','created_on')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

# register the NavigationListItem model and NavigationList model - no need for summernote
admin.site.register(NavigationList)