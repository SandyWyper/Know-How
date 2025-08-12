"""URL patterns for the listings app."""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.ListingList.as_view(), name="home"),
    path("create/", views.ListingCreateView.as_view(), name="listing_create"),
    path("<slug:slug>/edit/", views.ListingUpdateView.as_view(), name="listing_edit"),
    path("<slug:slug>/delete/", views.ListingDeleteView.as_view(), name="listing_delete"),
    path("<slug:slug>/publish/", views.publish_listing, name="listing_publish"),
    path('<slug:slug>/', views.listing_detail, name='listing_detail'),
]

