from django.contrib import admin

# Register your models here.
from .models import Listing
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Listing)
class ListingAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on', 'updated_on')
    search_fields = ['title']
    list_filter = ('status','created_on')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)
# Register your models here.
# admin.site.register(Listing)