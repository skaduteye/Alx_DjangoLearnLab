from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Library, Book


def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect


def user_login(request):
    from django.contrib.auth.views import LoginView
    return LoginView.as_view(template_name='relationship_app/login.html')(request)


def user_logout(request):
    from django.contrib.auth.views import LogoutView
    return LogoutView.as_view(template_name='relationship_app/logout.html')(request)


def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    return render(request, 'relationship_app/register.html', {'form': form})
