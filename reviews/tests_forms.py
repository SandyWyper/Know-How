from django.test import TestCase
from django.contrib.auth.models import User
from profiles.forms import ReviewForm  # ReviewForm is in profiles app
from .models import Review


class TestReviewFormIntegration(TestCase):
    """Integration tests for ReviewForm with Review model validation."""

    def setUp(self):
        """Set up test data."""
        self.author = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='testpass123'
        )
        
        self.target_user = User.objects.create_user(
            username='tutor',
            email='tutor@example.com',
            password='testpass123'
        )
        
        self.valid_form_data = {
            'rating': 8,
            'title': 'Great tutor!',
            'body': 'I learned so much from this tutor. Highly recommend!'
        }

    def test_review_model_validation_with_form(self):
        """Test that Review model validation works with form data."""
        form = ReviewForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        
        review = form.save(commit=False)
        review.author = self.author
        review.target_user = self.target_user
        
        # Should not raise validation error
        review.full_clean()
        review.save()
        
        self.assertEqual(Review.objects.count(), 1)

    def test_review_unique_constraint_enforcement(self):
        """Test that unique constraint (author, target_user) is enforced."""
        # Create first review
        Review.objects.create(
            rating=8,
            title='First review',
            body='First review body',
            author=self.author,
            target_user=self.target_user
        )
        
        # Try to create second review with same author and target_user
        form = ReviewForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        
        review = form.save(commit=False)
        review.author = self.author
        review.target_user = self.target_user
        
        # Should raise IntegrityError when trying to save
        with self.assertRaises(Exception):  # IntegrityError or similar
            review.save()

    def test_review_rating_model_validation(self):
        """Test that model-level rating validation works."""
        # Test rating below minimum
        form_data = self.valid_form_data.copy()
        form_data['rating'] = 0
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        
        # Test rating above maximum
        form_data['rating'] = 11
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_review_str_representation(self):
        """Test the string representation of Review model."""
        form = ReviewForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        
        review = form.save(commit=False)
        review.author = self.author
        review.target_user = self.target_user
        review.save()
        
        expected_str = f"Review by {self.author} for {self.target_user} ({review.rating}/10)"
        self.assertEqual(str(review), expected_str)

    def test_review_ordering(self):
        """Test that reviews are ordered by creation date (most recent first)."""
        # Create multiple reviews with different target users to avoid unique constraint
        target_user2 = User.objects.create_user(
            username='tutor2',
            email='tutor2@example.com',
            password='testpass123'
        )
        
        # Create first review
        review1 = Review.objects.create(
            rating=8,
            title='First review',
            body='First review body',
            author=self.author,
            target_user=self.target_user
        )
        
        # Create second review
        review2 = Review.objects.create(
            rating=9,
            title='Second review',
            body='Second review body',
            author=self.author,
            target_user=target_user2
        )
        
        # Get all reviews - should be ordered by creation date (newest first)
        reviews = Review.objects.all()
        self.assertEqual(reviews[0], review2)  # Most recent first
        self.assertEqual(reviews[1], review1)

    def test_review_title_max_length_constraint(self):
        """Test that title field enforces max length constraint."""
        form_data = self.valid_form_data.copy()
        form_data['title'] = 'x' * 101  # Exceeds 100 character limit
        
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_review_fields_are_required(self):
        """Test that required fields are properly validated."""
        required_fields = ['rating', 'title', 'body']
        
        for field in required_fields:
            form_data = self.valid_form_data.copy()
            del form_data[field]
            
            form = ReviewForm(data=form_data)
            self.assertFalse(form.is_valid(), f"Form should be invalid without {field}")
            self.assertIn(field, form.errors, f"Should have error for missing {field}")

    def test_review_foreign_key_relationships(self):
        """Test that foreign key relationships work correctly."""
        form = ReviewForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        
        review = form.save(commit=False)
        review.author = self.author
        review.target_user = self.target_user
        review.save()
        
        # Test author relationship
        self.assertEqual(review.author, self.author)
        self.assertIn(review, self.author.reviews_written.all())
        
        # Test target_user relationship
        self.assertEqual(review.target_user, self.target_user)
        self.assertIn(review, self.target_user.reviews_received.all())

    def test_review_timestamps(self):
        """Test that timestamps are set correctly."""
        form = ReviewForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        
        review = form.save(commit=False)
        review.author = self.author
        review.target_user = self.target_user
        review.save()
        
        # created_on should be set
        self.assertIsNotNone(review.created_on)
        
        # updated_on should be set
        self.assertIsNotNone(review.updated_on)
        
        # Both should be approximately equal for new review
        time_diff = abs((review.updated_on - review.created_on).total_seconds())
        self.assertLess(time_diff, 1)  # Less than 1 second difference

    def test_review_update_timestamp(self):
        """Test that updated_on timestamp changes when review is updated."""
        form = ReviewForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        
        review = form.save(commit=False)
        review.author = self.author
        review.target_user = self.target_user
        review.save()
        
        original_updated = review.updated_on
        
        # Update the review
        review.title = 'Updated title'
        review.save()
        
        # updated_on should have changed
        self.assertNotEqual(review.updated_on, original_updated)
        self.assertGreater(review.updated_on, original_updated)

    def test_form_integration_with_existing_review(self):
        """Test form works correctly when editing existing review."""
        # Create existing review
        existing_review = Review.objects.create(
            rating=5,
            title='Original title',
            body='Original body',
            author=self.author,
            target_user=self.target_user
        )
        
        # Update data
        update_data = {
            'rating': 9,
            'title': 'Updated title',
            'body': 'Updated body content'
        }
        
        form = ReviewForm(data=update_data, instance=existing_review)
        self.assertTrue(form.is_valid())
        
        updated_review = form.save()
        
        # Check that the review was updated, not created new
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(updated_review.pk, existing_review.pk)
        self.assertEqual(updated_review.rating, 9)
        self.assertEqual(updated_review.title, 'Updated title')
        self.assertEqual(updated_review.body, 'Updated body content')
        
        # Author and target_user should remain the same
        self.assertEqual(updated_review.author, self.author)
        self.assertEqual(updated_review.target_user, self.target_user)
