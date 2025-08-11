from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import DetailView, UpdateView
from django.urls import reverse

from .models import UserProfile
from reviews.models import Review
from .forms import UserProfileForm, ReviewForm

class ProfileDetailView(DetailView):
    """Display a user's profile page with their reviews and review form."""
    model = User
    template_name = 'profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        
        # Get user's reviews received
        context['reviews'] = user.reviews_received.all()
        context['total_reviews'] = user.reviews_received.count()
        
        # Get user's listings if they're a tutor
        context['listings'] = user.listings.filter(status=1)[:5]  # Latest 5 published listings
        
        # Check if current user can leave a review and add review form
        if self.request.user.is_authenticated and self.request.user != user:
            existing_review = Review.objects.filter(
                author=self.request.user, 
                target_user=user
            ).first()
            
            if existing_review:
                context['user_review'] = existing_review
                context['can_review'] = False
            else:
                context['can_review'] = True
                context['review_form'] = ReviewForm()
        else:
            context['can_review'] = False
            
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle review submission."""
        user = self.get_object()
        
        # Check if user is authenticated and not reviewing themselves
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to leave a review.")
            return redirect('profiles:profile', username=user.username)
        
        if request.user == user:
            messages.error(request, "You cannot review yourself.")
            return redirect('profiles:profile', username=user.username)
        
        # Check if user has already reviewed this person
        if Review.objects.filter(author=request.user, target_user=user).exists():
            messages.error(request, "You have already reviewed this user.")
            return redirect('profiles:profile', username=user.username)
        
        # Process the review form
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.target_user = user
            review.save()
            messages.success(request, "Your review has been submitted successfully!")
            return redirect('profiles:profile', username=user.username)
        else:
            # If form is invalid, reload the page with errors
            messages.error(request, "There was an error with your review. Please check the form.")
            return self.get(request, *args, **kwargs)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Allow users to edit their own profile."""
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'profile_edit.html'
    
    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)
    
    def get_success_url(self):
        return reverse('profiles:profile', kwargs={'username': self.request.user.username})
