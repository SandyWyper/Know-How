from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    # Profile views
    path('<str:username>/', views.ProfileDetailView.as_view(), name='profile'),
    path('<str:username>/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
]