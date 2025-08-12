from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Listing
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .forms import ListingForm
from django.http import Http404  # added
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
    """
    listing = get_object_or_404(Listing, slug=slug)

    # Allow only published listings, or draft if owner/staff
    if listing.status != 1:
        if not (request.user.is_authenticated and (request.user == listing.tutor or request.user.is_staff or request.user.is_superuser)):
            raise Http404("Listing not found")

    return render(request, "listings/listing_detail.html", {"listing": listing})


class ListingCreateView(LoginRequiredMixin, generic.CreateView):
    """Create a new listing for the logged-in user."""
    model = Listing
    form_class = ListingForm
    template_name = "listings/create_listing.html"

    def form_valid(self, form):
        form.instance.tutor = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("listing_detail", kwargs={"slug": self.object.slug})


class ListingUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Edit an existing listing (owner-only)."""
    model = Listing
    form_class = ListingForm
    template_name = "listings/create_listing.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        # Owner-only editing; staff can edit everything
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Listing.objects.all()
        return Listing.objects.filter(tutor=self.request.user)

    def get_success_url(self):
        return reverse("listing_detail", kwargs={"slug": self.object.slug})


@login_required
def publish_listing(request, slug):
    """Publish a listing (owner/staff only)."""
    listing = get_object_or_404(Listing, slug=slug)
    if not (request.user == listing.tutor or request.user.is_staff or request.user.is_superuser):
        raise Http404("Listing not found")

    if request.method == "POST":
        listing.status = 1
        listing.save(update_fields=["status", "updated_on"])
        messages.success(request, "Listing published.")
        return redirect("listing_detail", slug=listing.slug)

    return redirect("listing_detail", slug=listing.slug)