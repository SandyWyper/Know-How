from django.shortcuts import render
from django.views import generic
from .models import Listing

# Create your views here.
class ListingList(generic.ListView):
    """Displays a list of published listings."""
    queryset = Listing.objects.filter(status=1).order_by("-created_on")
    template_name = "listings/index.html"
    paginate_by = 6
    # context_object_name = "object_list"
