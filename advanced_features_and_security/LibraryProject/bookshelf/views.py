from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book

# View all books (requires can_view permission)
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/view_books.html', {'books': books})

# Create a book (requires can_create permission)
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        published_date = request.POST.get('published_date')
        Book.objects.create(title=title, author=author, published_date=published_date)
        return redirect('view_books')
    return render(request, 'bookshelf/create_book.html')

# Edit a book (requires can_edit permission)
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.title = request.POST.get('title', book.title)
        book.author = request.POST.get('author', book.author)
        book.published_date = request.POST.get('published_date', book.published_date)
        book.save()
        return redirect('view_books')
    return render(request, 'bookshelf/edit_book.html', {'book': book})

# Delete a book (requires can_delete permission)
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('view_books')
    return render(request, 'bookshelf/delete_book.html', {'book': book})

# Documentation note:
# To set up groups and assign permissions, use Django admin:
# 1. Create groups: Editors, Viewers, Admins
# 2. Assign permissions (can_view, can_create, can_edit, can_delete) to each group
# 3. Add users to groups as needed
# Only users with the correct permissions will be able to access the corresponding views.
