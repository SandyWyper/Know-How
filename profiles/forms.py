from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML
from crispy_forms.bootstrap import FormActions

from .models import UserProfile
from reviews.models import Review

class UserProfileForm(forms.ModelForm):
    """Form for editing user profile."""
    
    # Add user fields that we want to edit
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)
    
    class Meta:
        model = UserProfile
        fields = [
            'bio', 'location', 'website', 'phone_number', 
            'profile_image', 'expertise_areas', 'years_experience', 
            'education', 'certifications', 'is_tutor', 
            'show_email_publicly', 'allow_reviews'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'expertise_areas': forms.Textarea(attrs={'rows': 3}),
            'education': forms.Textarea(attrs={'rows': 3}),
            'certifications': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Pre-populate user fields if editing existing profile
        if self.instance and self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
        
        # Crispy forms helper
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML('<h3 class="">Personal Information</h3>'),
                Div(
                    Field('first_name', wrapper_class='w-1/2 pr-2'),
                    Field('last_name', wrapper_class='w-1/2 pl-2'),
                    css_class='flex'
                ),
                'email',
                'bio',
                css_class='mb-6'
            ),
            Div(
                HTML('<h3 class="">Contact & Location</h3>'),
                'location',
                'website',
                'phone_number',
                'profile_image',
                css_class='mb-6'
            ),
            Div(
                HTML('<h3 class="">Professional Information</h3>'),
                'expertise_areas',
                'years_experience',
                'education',
                'certifications',
                css_class='mb-6'
            ),
            Div(
                HTML('<h3 class="">Settings</h3>'),
                'is_tutor',
                'show_email_publicly',
                'allow_reviews',
                css_class='mb-6'
            ),
            FormActions(
                Submit('submit', 'Update Profile', css_class='btn btn-primary')
            )
        )
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        
        if commit:
            # Save user fields
            user = profile.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
            
            # Save profile
            profile.save()
        
        return profile

class ReviewForm(forms.ModelForm):
    """Form for creating reviews."""
    
    class Meta:
        model = Review
        fields = ['rating', 'title', 'body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.Select(choices=[(i, f'{i}/10') for i in range(1, 11)])
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'rating',
            'title',
            'body',
            FormActions(
                Submit('submit', 'Submit Review', css_class='btn btn-primary')
            )
        )
