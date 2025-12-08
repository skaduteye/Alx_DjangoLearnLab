from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Post, Comment
from .forms import CustomUserCreationForm, UserUpdateForm, CommentForm, PostForm

# Create your views here.

def home(request):
    """Display all blog posts on the home page."""
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)


# Class-based views for Post CRUD operations

class PostListView(ListView):
    """Display all blog posts in a paginated list."""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 10


class PostDetailView(DetailView):
    """Display a single blog post with full details and comments."""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        """Add comments and comment form to the context."""
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['comment_form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Allow authenticated users to create new blog posts."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        """Set the post author to the current logged-in user."""
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect to the newly created post detail page."""
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allow post authors to edit their own posts."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        """Maintain the original author when updating."""
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        """Check if the current user is the author of the post."""
        post = self.get_object()
        return self.request.user == post.author
    
    def get_success_url(self):
        """Redirect to the updated post detail page."""
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allow post authors to delete their own posts."""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')
    
    def test_func(self):
        """Check if the current user is the author of the post."""
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        """Add success message when post is deleted."""
        messages.success(self.request, 'Your post has been deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Authentication views
def register(request):
    """Handle user registration with custom form including email."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}! You can now log in.')
            login(request, user)
            return redirect('blog-home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile(request):
    """Display and allow editing of user profile information."""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserUpdateForm(instance=request.user)
    
    context = {
        'form': form
    }
    return render(request, 'blog/profile.html', context)


# Comment views

class CommentCreateView(LoginRequiredMixin, CreateView):
    """Allow authenticated users to add comments to blog posts."""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        """Set the comment author and associated post."""
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        messages.success(self.request, 'Your comment has been posted successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect back to the post detail page."""
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['pk']})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allow comment authors to edit their own comments."""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        """Maintain the original author and post when updating."""
        messages.success(self.request, 'Your comment has been updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        """Check if the current user is the author of the comment."""
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        """Redirect back to the post detail page."""
        comment = self.get_object()
        return reverse_lazy('post-detail', kwargs={'pk': comment.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allow comment authors to delete their own comments."""
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def test_func(self):
        """Check if the current user is the author of the comment."""
        comment = self.get_object()
        return self.request.user == comment.author
    
    def delete(self, request, *args, **kwargs):
        """Add success message when comment is deleted."""
        messages.success(self.request, 'Your comment has been deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        """Redirect back to the post detail page."""
        comment = self.get_object()
        return reverse_lazy('post-detail', kwargs={'pk': comment.post.pk})


# Search and Tag views

def search_posts(request):
    """Search for posts by title, content, or tags."""
    query = request.GET.get('q', '')
    results = Post.objects.none()
    
    if query:
        # Use Q objects to search across multiple fields
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    context = {
        'query': query,
        'results': results,
        'count': results.count()
    }
    return render(request, 'blog/search_results.html', context)


class TaggedPostListView(ListView):
    """Display all posts with a specific tag."""
    model = Post
    template_name = 'blog/tagged_posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        """Filter posts by the tag name from the URL."""
        tag_name = self.kwargs.get('tag_name')
        return Post.objects.filter(tags__name__in=[tag_name])
    
    def get_context_data(self, **kwargs):
        """Add the tag name to the context."""
        context = super().get_context_data(**kwargs)
        context['tag_name'] = self.kwargs.get('tag_name')
        return context
