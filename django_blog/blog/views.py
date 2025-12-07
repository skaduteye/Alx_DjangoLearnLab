from django.shortcuts import render
from .models import Post

# Create your views here.

def home(request):
    """Display all blog posts on the home page."""
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)
