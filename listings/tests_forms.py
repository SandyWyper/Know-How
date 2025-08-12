from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from .forms import ListingForm, TimeSlotForm
from .models import Listing


class TestListingForm(TestCase):
    """Unit tests for `ListingForm` behavior and validation."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.valid_form_data = {
            'title': 'Python Programming Basics',
            'short_description': 'Learn Python from scratch',
            'location': 'Online',
            'session_time': '2 hours',
            'content': 'Comprehensive Python course covering variables, functions, and more.',
            'status': '0',  # Draft
        }
        
        self.valid_image = SimpleUploadedFile(
            name='test.jpg',
            content=b"fake-image-bytes",
            content_type='image/jpeg',
        )

    def test_form_is_valid_with_all_fields(self):
        """Test form validity with all fields provided."""
        form = ListingForm(data=self.valid_form_data, files={'image': self.valid_image})
        self.assertTrue(form.is_valid())

    def test_form_is_valid_with_minimum_required_fields(self):
        """Test form validity with only required fields."""
        minimal_data = {
            'title': 'Test Listing',
            'content': 'Test content',
            'status': '0',
        }
        form = ListingForm(data=minimal_data, files={'image': self.valid_image})
        self.assertTrue(form.is_valid())

    def test_form_invalid_without_title(self):
        """Test form is invalid without title."""
        form_data = self.valid_form_data.copy()
        del form_data['title']
        form = ListingForm(data=form_data, files={'image': self.valid_image})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_form_invalid_without_content(self):
        """Test form is invalid without content."""
        form_data = self.valid_form_data.copy()
        del form_data['content']
        form = ListingForm(data=form_data, files={'image': self.valid_image})
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

    def test_form_invalid_without_status(self):
        """Test form is invalid without status."""
        form_data = self.valid_form_data.copy()
        del form_data['status']
        form = ListingForm(data=form_data, files={'image': self.valid_image})
        self.assertFalse(form.is_valid())
        self.assertIn('status', form.errors)

    def test_form_valid_without_optional_fields(self):
        """Test form is valid without optional fields."""
        form_data = {
            'title': 'Test Listing',
            'content': 'Test content',
            'status': '0',
        }
        form = ListingForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_save_generates_slug(self):
        """Test that saving the form generates a unique slug."""
        # Test without image to avoid Cloudinary issues in tests
        form_data = self.valid_form_data.copy()
        form = ListingForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        # Mock the listing's tutor field since it's required
        listing = form.save(commit=False)
        listing.tutor = self.user
        listing.save()
        
        self.assertEqual(listing.slug, 'python-programming-basics')

    def test_form_save_generates_unique_slug_when_duplicate(self):
        """Test that saving the form generates unique slug when duplicate exists."""
        # Create existing listing with same title
        Listing.objects.create(
            title='Python Programming Basics',
            slug='python-programming-basics',
            tutor=self.user,
            content='Existing content'
        )
        
        # Test without image to avoid Cloudinary issues in tests
        form_data = self.valid_form_data.copy()
        form = ListingForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        listing = form.save(commit=False)
        listing.tutor = self.user
        listing.save()
        
        self.assertEqual(listing.slug, 'python-programming-basics-1')

    def test_form_save_preserves_existing_slug_on_update(self):
        """Test that updating a listing preserves its existing slug."""
        # Create existing listing
        existing_listing = Listing.objects.create(
            title='Original Title',
            slug='original-title',
            tutor=self.user,
            content='Original content'
        )
        
        # Update the listing
        update_data = self.valid_form_data.copy()
        form = ListingForm(data=update_data, instance=existing_listing)
        self.assertTrue(form.is_valid())
        
        updated_listing = form.save()
        self.assertEqual(updated_listing.slug, 'original-title')  # Should preserve original slug

    def test_form_status_choices(self):
        """Test that form accepts valid status choices."""
        # Test draft status
        form_data = self.valid_form_data.copy()
        form_data['status'] = '0'
        form = ListingForm(data=form_data, files={'image': self.valid_image})
        self.assertTrue(form.is_valid())
        
        # Test published status
        form_data['status'] = '1'
        form = ListingForm(data=form_data, files={'image': self.valid_image})
        self.assertTrue(form.is_valid())

    def test_form_invalid_status_choice(self):
        """Test that form rejects invalid status choices."""
        form_data = self.valid_form_data.copy()
        form_data['status'] = '2'  # Invalid status
        form = ListingForm(data=form_data, files={'image': self.valid_image})
        self.assertFalse(form.is_valid())
        self.assertIn('status', form.errors)


class TestTimeSlotForm(TestCase):
    """Unit tests for `TimeSlotForm` behavior and validation."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.listing = Listing.objects.create(
            title='Test Listing',
            slug='test-listing',
            tutor=self.user,
            content='Test content'
        )
        
        self.valid_form_data = {
            'start_time': '2024-12-01T10:00',
            'end_time': '2024-12-01T12:00',
            'event_spaces': 5,
            'event_spaces_available': 5,
        }

    def test_form_is_valid_with_all_fields(self):
        """Test form validity with all fields provided."""
        form = TimeSlotForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_without_start_time(self):
        """Test form is invalid without start_time."""
        form_data = self.valid_form_data.copy()
        del form_data['start_time']
        form = TimeSlotForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('start_time', form.errors)

    def test_form_invalid_without_end_time(self):
        """Test form is invalid without end_time."""
        form_data = self.valid_form_data.copy()
        del form_data['end_time']
        form = TimeSlotForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('end_time', form.errors)

    def test_form_invalid_without_event_spaces(self):
        """Test form is invalid without event_spaces."""
        form_data = self.valid_form_data.copy()
        del form_data['event_spaces']
        form = TimeSlotForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('event_spaces', form.errors)

    def test_form_invalid_without_event_spaces_available(self):
        """Test form is invalid without event_spaces_available."""
        form_data = self.valid_form_data.copy()
        del form_data['event_spaces_available']
        form = TimeSlotForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('event_spaces_available', form.errors)

    def test_form_accepts_valid_datetime_format(self):
        """Test form accepts valid datetime-local format."""
        form_data = {
            'start_time': '2024-12-01T10:00',
            'end_time': '2024-12-01T12:00',
            'event_spaces': 1,
            'event_spaces_available': 1,
        }
        form = TimeSlotForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_accepts_negative_event_spaces(self):
        """Test form accepts negative event_spaces (no validation constraint)."""
        form_data = self.valid_form_data.copy()
        form_data['event_spaces'] = -1
        form = TimeSlotForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_accepts_negative_event_spaces_available(self):
        """Test form accepts negative event_spaces_available (no validation constraint)."""
        form_data = self.valid_form_data.copy()
        form_data['event_spaces_available'] = -1
        form = TimeSlotForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_save_creates_timeslot(self):
        """Test that form save creates a TimeSlot instance."""
        form = TimeSlotForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        
        timeslot = form.save(commit=False)
        timeslot.listing = self.listing
        timeslot.save()
        
        self.assertEqual(timeslot.event_spaces, 5)
        self.assertEqual(timeslot.event_spaces_available, 5)
        self.assertTrue(timeslot.is_available)  # Default value