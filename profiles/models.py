from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

class UserProfile(models.Model):
    """Extended user profile information."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Profile information
    bio = models.TextField(max_length=500, blank=True, help_text="Tell others about yourself")
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    
    # Profile image
    profile_image = models.FileField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        help_text="Upload a profile picture"
    )
    
    # Professional information (since this seems to be a tutoring platform)
    expertise_areas = models.TextField(blank=True, help_text="Areas of expertise (comma-separated)")
    years_experience = models.PositiveIntegerField(null=True, blank=True)
    education = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    
    # Settings
    is_tutor = models.BooleanField(default=False, help_text="Can this user create listings?")
    show_email_publicly = models.BooleanField(default=False)
    allow_reviews = models.BooleanField(default=True)
    
    # Timestamps
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_absolute_url(self):
        return reverse('profiles:profile', kwargs={'username': self.user.username})
    
    @property
    def average_rating(self):
        """Calculate average rating from reviews."""
        reviews = self.user.reviews_received.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return None
    
    @property
    def total_reviews(self):
        """Get total number of reviews."""
        return self.user.reviews_received.count()