from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    """
    Model representing a review left by one user for a tutor.
    """
    # The tutor being reviewed
    target_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews_received',
        help_text="The tutor being reviewed"
    )
    # The user who wrote the review
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews_written',
        help_text="The user who wrote this review"
    )
    # Rating out of 10
    rating = models.PositiveIntegerField(
        help_text="Rating out of 10",
        choices=[(i, str(i)) for i in range(1, 11)]
    )
    # Review content
    body = models.TextField(
        help_text="The review content"
    )
    # When the review was created
    created_on = models.DateTimeField(
        auto_now_add=True,
        help_text="When this review was created"
    )

    class Meta:
        ordering = ['-created_on']  # Most recent reviews first
        # Ensure a user can only review a tutor once
        unique_together = ['target_user', 'author']
    def __str__(self):
        return f"Review by {self.author.username} for {self.target_user.username} ({self.rating}/10)"