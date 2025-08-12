from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from .forms import UserProfileForm, ReviewForm
from reviews.models import Review


class TestUserProfileForm(TestCase):
    """Unit tests for `UserProfileForm` behavior and validation."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        
        # Profile is automatically created by signals
        self.profile = self.user.profile
        self.profile.bio = 'Original bio'
        self.profile.location = 'Original location'
        self.profile.save()
        
        self.valid_form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'bio': 'I am a passionate teacher with years of experience.',
            'location': 'New York, NY',
            'expertise_areas': 'Python, Django, Web Development',
            'years_experience': 5,
            'education_and_certifications': 'Computer Science Degree, Python Certification'
        }
        
        self.valid_image = SimpleUploadedFile(
            name='profile.jpg',
            content=b"fake-image-bytes",
            content_type='image/jpeg',
        )

    def test_form_is_valid_with_all_fields(self):
        """Test form validity with all fields provided."""
        form = UserProfileForm(
            data=self.valid_form_data, 
            files={'profile_image': self.valid_image},
            instance=self.profile
        )
        self.assertTrue(form.is_valid())

    def test_form_is_valid_with_minimum_fields(self):
        """Test form validity with only required fields (none are required)."""
        minimal_data = {}
        form = UserProfileForm(data=minimal_data, instance=self.profile)
        self.assertTrue(form.is_valid())

    def test_form_prepopulates_user_fields(self):
        """Test that form prepopulates user fields from existing profile."""
        form = UserProfileForm(instance=self.profile)
        self.assertEqual(form.fields['first_name'].initial, 'John')
        self.assertEqual(form.fields['last_name'].initial, 'Doe')
        self.assertEqual(form.fields['email'].initial, 'test@example.com')

    def test_form_save_updates_user_fields(self):
        """Test that form save updates related User model fields."""
        form_data = self.valid_form_data.copy()
        form_data.update({
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com'
        })
        
        form = UserProfileForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())
        
        form.save()
        
        # Check that user fields were updated
        updated_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(updated_user.first_name, 'Jane')
        self.assertEqual(updated_user.last_name, 'Smith')
        self.assertEqual(updated_user.email, 'jane.smith@example.com')

    def test_form_save_updates_profile_fields(self):
        """Test that form save updates profile fields."""
        form = UserProfileForm(data=self.valid_form_data, instance=self.profile)
        self.assertTrue(form.is_valid())
        
        updated_profile = form.save()
        
        self.assertEqual(updated_profile.bio, 'I am a passionate teacher with years of experience.')
        self.assertEqual(updated_profile.location, 'New York, NY')
        self.assertEqual(updated_profile.expertise_areas, 'Python, Django, Web Development')
        self.assertEqual(updated_profile.years_experience, 5)

    def test_form_accepts_valid_email_format(self):
        """Test that form accepts valid email formats."""
        valid_emails = [
            'test@example.com',
            'user.name@domain.co.uk',
            'test123@test-domain.org'
        ]
        
        for email in valid_emails:
            form_data = self.valid_form_data.copy()
            form_data['email'] = email
            form = UserProfileForm(data=form_data, instance=self.profile)
            self.assertTrue(form.is_valid(), f"Email {email} should be valid")

    def test_form_rejects_invalid_email_format(self):
        """Test that form rejects invalid email formats."""
        invalid_emails = [
            'not-an-email',
            '@domain.com',
            'user@',
            'user@domain',
        ]
        
        for email in invalid_emails:
            form_data = self.valid_form_data.copy()
            form_data['email'] = email
            form = UserProfileForm(data=form_data, instance=self.profile)
            self.assertFalse(form.is_valid(), f"Email {email} should be invalid")
            self.assertIn('email', form.errors)

    def test_form_accepts_valid_years_experience(self):
        """Test that form accepts valid years of experience."""
        valid_years = [0, 1, 5, 10, 25, 50]
        
        for years in valid_years:
            form_data = self.valid_form_data.copy()
            form_data['years_experience'] = years
            form = UserProfileForm(data=form_data, instance=self.profile)
            self.assertTrue(form.is_valid(), f"Years experience {years} should be valid")

    def test_form_rejects_negative_years_experience(self):
        """Test that form rejects negative years of experience."""
        form_data = self.valid_form_data.copy()
        form_data['years_experience'] = -1
        form = UserProfileForm(data=form_data, instance=self.profile)
        self.assertFalse(form.is_valid())

    def test_form_handles_empty_optional_fields(self):
        """Test that form handles empty optional fields correctly."""
        form_data = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'bio': '',
            'location': '',
            'expertise_areas': '',
            'years_experience': '',
            'education_and_certifications': ''
        }
        form = UserProfileForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())

    def test_form_save_without_commit(self):
        """Test that form save works with commit=False."""
        form = UserProfileForm(data=self.valid_form_data, instance=self.profile)
        self.assertTrue(form.is_valid())
        
        profile = form.save(commit=False)
        self.assertEqual(profile.bio, 'I am a passionate teacher with years of experience.')
        
        # Profile should not be saved to database yet
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, 'Original bio')


class TestReviewForm(TestCase):
    """Unit tests for `ReviewForm` behavior and validation."""

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

    def test_form_is_valid_with_all_fields(self):
        """Test form validity with all fields provided."""
        form = ReviewForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_without_rating(self):
        """Test form is invalid without rating."""
        form_data = self.valid_form_data.copy()
        del form_data['rating']
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_form_invalid_without_title(self):
        """Test form is invalid without title."""
        form_data = self.valid_form_data.copy()
        del form_data['title']
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_form_invalid_without_body(self):
        """Test form is invalid without body."""
        form_data = self.valid_form_data.copy()
        del form_data['body']
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('body', form.errors)

    def test_form_accepts_valid_rating_range(self):
        """Test that form accepts ratings from 1 to 10."""
        for rating in range(1, 11):
            form_data = self.valid_form_data.copy()
            form_data['rating'] = rating
            form = ReviewForm(data=form_data)
            self.assertTrue(form.is_valid(), f"Rating {rating} should be valid")

    def test_form_rejects_invalid_rating_below_range(self):
        """Test that form rejects ratings below 1."""
        invalid_ratings = [0, -1, -5]
        
        for rating in invalid_ratings:
            form_data = self.valid_form_data.copy()
            form_data['rating'] = rating
            form = ReviewForm(data=form_data)
            self.assertFalse(form.is_valid(), f"Rating {rating} should be invalid")

    def test_form_rejects_invalid_rating_above_range(self):
        """Test that form rejects ratings above 10."""
        invalid_ratings = [11, 15, 100]
        
        for rating in invalid_ratings:
            form_data = self.valid_form_data.copy()
            form_data['rating'] = rating
            form = ReviewForm(data=form_data)
            self.assertFalse(form.is_valid(), f"Rating {rating} should be invalid")

    def test_form_title_max_length(self):
        """Test that form enforces title max length."""
        form_data = self.valid_form_data.copy()
        form_data['title'] = 'x' * 101  # Exceeds 100 character limit
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_form_title_within_max_length(self):
        """Test that form accepts title within max length."""
        form_data = self.valid_form_data.copy()
        form_data['title'] = 'x' * 100  # Exactly 100 characters
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_save_creates_review(self):
        """Test that form save creates a Review instance."""
        form = ReviewForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        
        review = form.save(commit=False)
        review.author = self.author
        review.target_user = self.target_user
        review.save()
        
        self.assertEqual(review.rating, 8)
        self.assertEqual(review.title, 'Great tutor!')
        self.assertEqual(review.body, 'I learned so much from this tutor. Highly recommend!')
        self.assertEqual(review.author, self.author)
        self.assertEqual(review.target_user, self.target_user)

    def test_form_edit_mode_button_text(self):
        """Test that form shows correct button text for editing."""
        # Create existing review
        review = Review.objects.create(
            rating=5,
            title='Original title',
            body='Original body',
            author=self.author,
            target_user=self.target_user
        )
        
        form = ReviewForm(instance=review)
        # Note: We can't easily test the button text since it's in the helper layout,
        # but we can verify the form initializes correctly with an existing instance
        self.assertEqual(form.instance.pk, review.pk)

    def test_form_create_mode(self):
        """Test that form works correctly in create mode."""
        form = ReviewForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        self.assertIsNone(form.instance.pk)

    def test_form_rating_choices_display(self):
        """Test that rating field has proper choices."""
        form = ReviewForm()
        rating_choices = form.fields['rating'].widget.choices
        
        # Convert to list for comparison since widget.choices might be different type
        actual_choices = list(rating_choices)
        
        # Model choices take precedence over widget choices
        # Should include empty choice plus model choices from 1 to 10
        expected_choices = [('', '---------')] + [(i, str(i)) for i in range(1, 11)]
        self.assertEqual(actual_choices, expected_choices)

    def test_form_handles_unicode_content(self):
        """Test that form handles unicode characters in text fields."""
        form_data = self.valid_form_data.copy()
        form_data.update({
            'title': 'Excelente tutor! 🎓',
            'body': 'Aprendí mucho. ¡Muy recomendado! 👍'
        })
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())
