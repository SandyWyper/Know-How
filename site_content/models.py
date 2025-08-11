from django.db import models


STATUS = ((0, "Draft"), (1, "Published"))
# Create your models here.

class Page(models.Model):
    """Model representing a static page."""
    title = models.CharField(max_length=100, unique=False)
    excerpt = models.TextField(blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return f"{self.title}"




class NavigationList(models.Model):
    """A model representing a list on navigation links"""
    list_name = models.CharField(max_length=100, unique=False)
    list = models.ManyToManyField(Page, related_name="links")

    def published_pages(self):
        """Return only published pages in this list"""
        return self.list.filter(status=1)
        
    def __str__(self):
        return f"{self.list_name}"
