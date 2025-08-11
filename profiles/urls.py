from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    # Profile views
    path('profile/<str:username>/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/<str:username>/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
]