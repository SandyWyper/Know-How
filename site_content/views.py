from django.shortcuts import render, get_object_or_404
from .models import Page

# Create your views here.
def page_content(request, slug):
    """
    Displays a static page.
    """
    queryset = Page.objects.filter(status=1)
    page = get_object_or_404(queryset, slug=slug)


    return render(request, "page_default.html", {"page": page})