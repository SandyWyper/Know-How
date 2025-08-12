from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('<int:pk>/edit/', views.ReviewEditView.as_view(), name='edit'),
]
