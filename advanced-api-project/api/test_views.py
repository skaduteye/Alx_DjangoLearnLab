"""
Unit Tests for Django REST Framework API Views

This module contains comprehensive unit tests for all API endpoints in the advanced-api-project.
Tests cover CRUD operations, filtering, searching, ordering, authentication, and permissions.

Django's test framework automatically creates a separate test database for running tests,
ensuring that production/development data is never affected. The test database is created
before tests run and destroyed afterward.

Test Categories:
1. Book CRUD Operations (Create, Read, Update, Delete)
2. Filtering functionality
3. Searching functionality
4. Ordering functionality
5. Authentication and Permissions

Run tests with: python manage.py test api

Note: These tests use Token Authentication (REST Framework's token-based auth) rather than
session-based authentication (self.client.login). Token auth is more appropriate for API testing.
"""

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from .models import Author, Book


class BookAPITestCase(APITestCase):
    """
    Base test case class with common setup for all Book API tests.
    Creates test data and provides helper methods for authentication.
    
    Note: APITestCase automatically uses a separate test database that is created
    at the start of the test run and destroyed at the end, ensuring no impact on
    production or development data.
    """
    
    def setUp(self):
        """
        Set up test data before each test method.
        Creates users, authors, books, and authentication tokens.
        
        This method runs before each test, ensuring a clean state with fresh test data.
        All data is created in the test database, which is separate from production/dev.
        """
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        
        # Create authentication tokens for API authentication
        self.token = Token.objects.create(user=self.user)
        self.other_token = Token.objects.create(user=self.other_user)
        
        # Configure test database - Django automatically uses a separate test database
        # This can also be configured in settings with TEST database settings
        
        # Example of session-based login (alternative to token auth):
        # logged_in = self.client.login(username='testuser', password='testpass123')
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George R.R. Martin')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='Harry Potter and the Chamber of Secrets',
            publication_year=1998,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title='A Game of Thrones',
            publication_year=1996,
            author=self.author2
        )
        
        # Initialize API client
        self.client = APIClient()
        
        # Demonstrate self.client.login for session-based authentication
        # (Though token auth is used in these tests, this shows the alternative)
        # self.client.login(username='testuser', password='testpass123')
    
    def authenticate(self, token=None):
        """Helper method to authenticate requests with a token."""
        if token is None:
            token = self.token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    
    def unauthenticate(self):
        """Helper method to remove authentication credentials."""
        self.client.credentials()


class BookListViewTests(BookAPITestCase):
    """Tests for the BookListView endpoint (GET /api/books/)"""
    
    def test_list_books_unauthenticated(self):
        """Test that unauthenticated users can list books (public access)."""
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Should return all 3 books
    
    def test_list_books_authenticated(self):
        """Test that authenticated users can list books."""
        self.authenticate()
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_list_books_returns_correct_data(self):
        """Test that book list returns correct book data."""
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that response contains expected book titles
        titles = [book['title'] for book in response.data]
        self.assertIn('Harry Potter and the Philosopher\'s Stone', titles)
        self.assertIn('A Game of Thrones', titles)


class BookDetailViewTests(BookAPITestCase):
    """Tests for the BookDetailView endpoint (GET /api/books/<pk>/)"""
    
    def test_retrieve_book_unauthenticated(self):
        """Test that unauthenticated users can retrieve a single book."""
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
    
    def test_retrieve_nonexistent_book(self):
        """Test that retrieving a nonexistent book returns 404."""
        url = reverse('book-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_retrieve_book_authenticated(self):
        """Test that authenticated users can retrieve a book."""
        self.authenticate()
        url = reverse('book-detail', kwargs={'pk': self.book2.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book2.title)


class BookCreateViewTests(BookAPITestCase):
    """Tests for the BookCreateView endpoint (POST /api/books/create/)"""
    
    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create books."""
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'publication_year': 2020,
            'author': self.author1.pk
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_book_authenticated(self):
        """Test that authenticated users can create books."""
        self.authenticate()
        url = reverse('book-create')
        data = {
            'title': 'The Hobbit',
            'publication_year': 1937,
            'author': self.author1.pk
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)  # 3 existing + 1 new
        self.assertEqual(response.data['title'], 'The Hobbit')
        self.assertEqual(response.data['publication_year'], 1937)
    
    def test_create_book_with_future_year(self):
        """Test that creating a book with future publication year fails validation."""
        self.authenticate()
        url = reverse('book-create')
        data = {
            'title': 'Future Book',
            'publication_year': 2030,
            'author': self.author1.pk
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_create_book_missing_required_fields(self):
        """Test that creating a book without required fields fails."""
        self.authenticate()
        url = reverse('book-create')
        data = {
            'title': 'Incomplete Book'
            # Missing publication_year and author
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BookUpdateViewTests(BookAPITestCase):
    """Tests for the BookUpdateView endpoint (PUT/PATCH /api/books/<pk>/update/)"""
    
    def test_update_book_unauthenticated(self):
        """Test that unauthenticated users cannot update books."""
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {'title': 'Updated Title'}
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_partial_update_book_authenticated(self):
        """Test that authenticated users can partially update books (PATCH)."""
        self.authenticate()
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {'title': 'Harry Potter and the Sorcerer\'s Stone'}
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Harry Potter and the Sorcerer\'s Stone')
        # Verify other fields unchanged
        self.assertEqual(self.book1.publication_year, 1997)
    
    def test_full_update_book_authenticated(self):
        """Test that authenticated users can fully update books (PUT)."""
        self.authenticate()
        url = reverse('book-update', kwargs={'pk': self.book3.pk})
        data = {
            'title': 'A Clash of Kings',
            'publication_year': 1998,
            'author': self.author2.pk
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book3.refresh_from_db()
        self.assertEqual(self.book3.title, 'A Clash of Kings')
        self.assertEqual(self.book3.publication_year, 1998)
    
    def test_update_nonexistent_book(self):
        """Test that updating a nonexistent book returns 404."""
        self.authenticate()
        url = reverse('book-update', kwargs={'pk': 9999})
        data = {'title': 'Updated Title'}
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_book_with_invalid_year(self):
        """Test that updating with future year fails validation."""
        self.authenticate()
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {'publication_year': 2030}
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BookDeleteViewTests(BookAPITestCase):
    """Tests for the BookDeleteView endpoint (DELETE /api/books/<pk>/delete/)"""
    
    def test_delete_book_unauthenticated(self):
        """Test that unauthenticated users cannot delete books."""
        url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Book.objects.filter(pk=self.book1.pk).exists())
    
    def test_delete_book_authenticated(self):
        """Test that authenticated users can delete books."""
        self.authenticate()
        url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())
        self.assertEqual(Book.objects.count(), 2)  # 3 - 1 deleted
    
    def test_delete_nonexistent_book(self):
        """Test that deleting a nonexistent book returns 404."""
        self.authenticate()
        url = reverse('book-delete', kwargs={'pk': 9999})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookFilteringTests(BookAPITestCase):
    """Tests for filtering functionality on BookListView"""
    
    def test_filter_by_title(self):
        """Test filtering books by exact title."""
        url = reverse('book-list')
        response = self.client.get(url, {'title': 'A Game of Thrones'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'A Game of Thrones')
    
    def test_filter_by_author_name(self):
        """Test filtering books by author name."""
        url = reverse('book-list')
        response = self.client.get(url, {'author__name': 'J.K. Rowling'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both Harry Potter books
        
        # Verify both books are by J.K. Rowling
        for book in response.data:
            self.assertEqual(book['author'], self.author1.pk)
    
    def test_filter_by_publication_year(self):
        """Test filtering books by publication year."""
        url = reverse('book-list')
        response = self.client.get(url, {'publication_year': 1997})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['publication_year'], 1997)
    
    def test_filter_with_no_results(self):
        """Test filtering with criteria that match no books."""
        url = reverse('book-list')
        response = self.client.get(url, {'publication_year': 2000})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    def test_filter_with_multiple_parameters(self):
        """Test filtering with multiple filter parameters."""
        url = reverse('book-list')
        response = self.client.get(url, {
            'author__name': 'J.K. Rowling',
            'publication_year': 1998
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter and the Chamber of Secrets')


class BookSearchTests(BookAPITestCase):
    """Tests for search functionality on BookListView"""
    
    def test_search_by_title(self):
        """Test searching books by title."""
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Harry'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both Harry Potter books
    
    def test_search_by_author_name(self):
        """Test searching books by author name."""
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Martin'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'A Game of Thrones')
    
    def test_search_case_insensitive(self):
        """Test that search is case-insensitive."""
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'potter'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_search_partial_match(self):
        """Test that search matches partial text."""
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Chamber'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter and the Chamber of Secrets')
    
    def test_search_no_results(self):
        """Test search with no matching results."""
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'NonexistentBook'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class BookOrderingTests(BookAPITestCase):
    """Tests for ordering functionality on BookListView"""
    
    def test_order_by_title_ascending(self):
        """Test ordering books by title in ascending order."""
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))
        self.assertEqual(titles[0], 'A Game of Thrones')
    
    def test_order_by_title_descending(self):
        """Test ordering books by title in descending order."""
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': '-title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles, reverse=True))
        self.assertEqual(titles[0], 'Harry Potter and the Philosopher\'s Stone')
    
    def test_order_by_publication_year_ascending(self):
        """Test ordering books by publication year in ascending order."""
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years))
        self.assertEqual(years, [1996, 1997, 1998])
    
    def test_order_by_publication_year_descending(self):
        """Test ordering books by publication year in descending order."""
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
        self.assertEqual(years, [1998, 1997, 1996])
    
    def test_default_ordering(self):
        """Test that default ordering is applied when no ordering parameter is provided."""
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Default ordering is by title (ascending)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))


class CombinedQueryTests(BookAPITestCase):
    """Tests for combining filtering, searching, and ordering"""
    
    def test_filter_and_search(self):
        """Test combining filtering and searching."""
        url = reverse('book-list')
        response = self.client.get(url, {
            'author__name': 'J.K. Rowling',
            'search': 'Chamber'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter and the Chamber of Secrets')
    
    def test_filter_and_ordering(self):
        """Test combining filtering and ordering."""
        url = reverse('book-list')
        response = self.client.get(url, {
            'author__name': 'J.K. Rowling',
            'ordering': '-publication_year'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Should be ordered by publication_year descending
        self.assertEqual(response.data[0]['publication_year'], 1998)
        self.assertEqual(response.data[1]['publication_year'], 1997)
    
    def test_search_and_ordering(self):
        """Test combining searching and ordering."""
        url = reverse('book-list')
        response = self.client.get(url, {
            'search': 'Harry',
            'ordering': 'publication_year'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, [1997, 1998])
    
    def test_filter_search_and_ordering(self):
        """Test combining all three: filtering, searching, and ordering."""
        url = reverse('book-list')
        response = self.client.get(url, {
            'author__name': 'J.K. Rowling',
            'search': 'Potter',
            'ordering': '-title'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Should be ordered by title descending
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles[0], 'Harry Potter and the Philosopher\'s Stone')


class PermissionTests(BookAPITestCase):
    """Tests for authentication and permission enforcement"""
    
    def test_session_based_authentication(self):
        """Test that session-based authentication works with client.login()."""
        # Demonstrate Django's session-based authentication for test database
        logged_in = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(logged_in)
        
        # Now use token auth for the actual API call
        self.authenticate()
        url = reverse('book-create')
        data = {'title': 'Session Auth Test', 'publication_year': 2020, 'author': self.author1.pk}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list_requires_no_authentication(self):
        """Test that listing books doesn't require authentication."""
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_detail_requires_no_authentication(self):
        """Test that retrieving a book doesn't require authentication."""
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_requires_authentication(self):
        """Test that creating a book requires authentication."""
        url = reverse('book-create')
        data = {'title': 'Test', 'publication_year': 2020, 'author': self.author1.pk}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_requires_authentication(self):
        """Test that updating a book requires authentication."""
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {'title': 'Updated'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_delete_requires_authentication(self):
        """Test that deleting a book requires authentication."""
        url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_different_user_can_modify_books(self):
        """Test that any authenticated user can modify books (no ownership restriction)."""
        # Create book as user 1
        self.authenticate(self.token)
        url = reverse('book-create')
        data = {'title': 'User1 Book', 'publication_year': 2020, 'author': self.author1.pk}
        response = self.client.post(url, data, format='json')
        book_id = response.data['id']
        
        # Update as user 2
        self.authenticate(self.other_token)
        url = reverse('book-update', kwargs={'pk': book_id})
        data = {'title': 'Modified by User2'}
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Modified by User2')
