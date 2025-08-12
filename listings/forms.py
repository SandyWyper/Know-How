from django import forms
from django.utils.text import slugify
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML
from crispy_forms.bootstrap import FormActions

from .models import Listing, TimeSlot


class ListingForm(forms.ModelForm):
    """Form for creating and editing listings."""
    
    class Meta:
        model = Listing
        fields = ['title', 'short_description', 'location', 'session_time', 'content', 'image', 'status']
        widgets = {
            'short_description': forms.Textarea(attrs={'rows': 3}),
            'content': forms.Textarea(attrs={'rows': 6}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        submit_text = 'Update Listing' if getattr(self.instance, 'pk', None) else 'Create Listing'

        # Crispy forms helper
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML('<h3 class="">Course Information</h3>'),
                Field('title', css_class='input input-bordered w-full'),
                Field('short_description', css_class='textarea textarea-bordered w-full'),
                Div(
                    Field('location', wrapper_class='w-1/2 pr-2', css_class='input input-bordered w-full'),
                    Field('session_time', wrapper_class='w-1/2 pl-2', css_class='input input-bordered w-full'),
                    css_class='flex flex-col sm:flex-row'
                ),
                Field('content', css_class='textarea textarea-bordered w-full'),
                HTML('<h3 class="mt-6">Image</h3>'),
                Field('image', css_class='file-input file-input-bordered w-full'),
                Field('status', css_class='select select-bordered w-full'),
                css_class='mb-6'
            ),
            FormActions(
                Submit('submit', submit_text, css_class='btn btn-primary')
            )
        )
    
    def save(self, commit=True):
        listing = super().save(commit=False)
        
        if not listing.slug:
            # Generate slug from title
            base_slug = slugify(listing.title)
            slug = base_slug
            counter = 1
            
            # Ensure slug is unique
            while Listing.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            listing.slug = slug
        
        if commit:
            listing.save()
        
        return listing


class TimeSlotForm(forms.ModelForm):
    """Form for creating time slots for listings."""
    
    class Meta:
        model = TimeSlot
        fields = ['start_time', 'end_time', 'event_spaces', 'event_spaces_available']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML('<h3 class="mb-4 text-lg font-semibold">Schedule Information</h3>'),
                Div(
                    Field('start_time', wrapper_class='w-1/2 pr-2', css_class='input input-bordered'),
                    Field('end_time', wrapper_class='w-1/2 pl-2', css_class='input input-bordered'),
                    css_class='flex'
                ),
                Div(
                    Field('event_spaces', wrapper_class='w-1/2 pr-2', css_class='input input-bordered'),
                    Field('event_spaces_available', wrapper_class='w-1/2 pl-2', css_class='input input-bordered'),
                    css_class='flex'
                ),
                css_class='mb-6'
            ),
            FormActions(
                Submit('submit', 'Add Time Slot', css_class='btn btn-secondary')
            )
        )
