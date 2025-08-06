from django.shortcuts import render
from django.views import generic
from .models import Listing

# Create your views here.
class ListingList(generic.ListView):
    model = Listing
    template_name = "listings/listings.html"
    # context_object_name = "object_list"
