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
    profile_image = models.ImageField(
        default='default_profile.jpg',
        upload_to='profile_pics/',
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
        return reverse('profile_detail', kwargs={'username': self.user.username})
    
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
    
    # Signal to auto-create profile when user is created
    @staticmethod
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
    
    @staticmethod
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

# Connect signals
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()