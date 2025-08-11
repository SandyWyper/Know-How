from django.db import models
from django.contrib.auth.models import User

STATUS = ((0, "Draft"), (1, "Published"))


# Create your models here.
class Listing(models.Model):
    """Model representing a tutoring listing or event."""
    title = models.CharField(max_length=100, unique=False)
    short_description = models.TextField(blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    tutor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings"
    )
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return f"{self.title} --- by {self.tutor.username}"



class TimeSlot(models.Model):
    """Model representing a time slot for a listing."""
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="time_slots")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event_spaces = models.IntegerField(default=1)
    event_spaces_available = models.IntegerField(default=1)
    is_available = models.BooleanField(default=True)
    status = models.IntegerField(choices=STATUS, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.listing.title} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

