"""URL patterns for the site_content app."""
from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>/', views.page_content, name='page_content'),
]