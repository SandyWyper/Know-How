from django.shortcuts import render
from django.views import generic
from .models import Listing

# Create your views here.
class ListingList(generic.ListView):
    queryset = Listing.objects.filter(status=1)
    template_name = "listings/listings.html"
    # context_object_name = "object_list"
