from django.db import models
from django.db.models.manager import Manager
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    # Explicit manager annotation for linters/type checkers
    objects: Manager = models.Manager()
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
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Rating out of 10",
        choices=[(i, str(i)) for i in range(1, 11)]
    )
    # Review content
    title = models.CharField(max_length=100, help_text="Review title")
    body = models.TextField(
        help_text="The review content"
    )
    # When the review was created
    created_on = models.DateTimeField(
        auto_now_add=True,
        help_text="When this review was created"
    )
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']  # Most recent reviews first
        unique_together = ['target_user', 'author'] # Ensure a user can only review a tutor once

    def __str__(self):
        # Simple and safe string conversion without attribute assumptions
        return f"Review by {self.author} for {self.target_user} ({self.rating}/10)"