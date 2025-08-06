from django.urls import path
from . import views

urlpatterns = [
    path("", views.ListingList.as_view(), name="home"),
]