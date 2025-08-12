"""URL patterns for the listings app."""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.ListingList.as_view(), name="home"),
    path("create/", views.ListingCreateView.as_view(), name="listing_create"),
    path('<slug:slug>/', views.listing_detail, name='listing_detail'),
]

