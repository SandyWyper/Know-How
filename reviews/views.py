from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import UpdateView
from django.urls import reverse
from .models import Review
from profiles.forms import ReviewForm

class ReviewEditView(LoginRequiredMixin, UpdateView):
    """Allow users to edit their own reviews."""
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/edit_review.html'
    
    def get_object(self, queryset=None):
        """Get the review object, ensuring user owns it."""
        review = get_object_or_404(Review, pk=self.kwargs['pk'])
        
        # Ensure the current user is the author of the review
        if review.author != self.request.user:
            messages.error(self.request, "You can only edit your own reviews.")
            return redirect('profiles:profile', username=review.target_user.username)
        
        return review
    
    def get_success_url(self):
        """Redirect back to the profile page after successful edit."""
        return reverse('profiles:profile', kwargs={'username': self.object.target_user.username})
    
    def form_valid(self, form):
        """Handle successful form submission."""
        messages.success(self.request, "Your review has been updated successfully!")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        """Add extra context to the template."""
        context = super().get_context_data(**kwargs)
        context['target_user'] = self.object.target_user
        return context
