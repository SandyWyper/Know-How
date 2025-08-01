from django.db import models
from django.contrib.auth.models import User

STATUS = ((0, "Draft"), (1, "Published"))


# Create your models here.
class Listing(models.Model):
    """Model representing a tutoring listing or event."""
    title = models.CharField(max_length=100, unique=False)
    slug = models.SlugField(max_length=200, unique=True)
    tutor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings"
    )
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    event_date_start = models.DateTimeField(null=True, blank=True)
    event_date_end = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(choices=STATUS, default=0)
