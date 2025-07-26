from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    """returns a simple "Hello, World!" response"""
    return HttpResponse("This was a " + request.method + " request, hello listings page!")