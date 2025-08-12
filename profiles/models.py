from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from cloudinary.models import CloudinaryField

class UserProfile(models.Model):
    """Extended user profile information."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Profile information
    bio = models.TextField(max_length=500, blank=True, help_text="Tell others about yourself")
    location = models.CharField(max_length=100, blank=True)
    
    # Profile image
    profile_image = CloudinaryField('image', default='placeholder')
    
    # Professional information
    expertise_areas = models.TextField(blank=True, help_text="Areas of expertise (comma-separated)")
    years_experience = models.PositiveIntegerField(null=True, blank=True)
    education_and_certifications = models.TextField(blank=True, help_text="Education background and certifications")
    
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