from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Listing

# Create your views here.
class ListingList(generic.ListView):
    """Displays a list of published listings."""
    queryset = Listing.objects.filter(status=1).order_by("-created_on")
    template_name = "listings/index.html"
    paginate_by = 6
    # context_object_name = "object_list"


def listing_detail(request, slug):
    """
    Displays a single listing.

    **Context**

    ``listing``
        An instance of :model:`listings.Listing`.

    **Template**
    
    :template:`listings/listing_detail.html`
    """

    queryset = Listing.objects.filter(status=1)
    listing = get_object_or_404(queryset, slug=slug)

    return render(request, "listings/listing_detail.html", {"listing": listing})