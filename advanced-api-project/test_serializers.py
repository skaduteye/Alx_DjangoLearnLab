"""
Test script for validating custom serializers
"""
from api.models import Author, Book
from api.serializers import BookSerializer

# Test validation for future publication year
author = Author.objects.get(id=1)
data = {
    'title': 'Future Book',
    'publication_year': 2030,
    'author': author.id
}

serializer = BookSerializer(data=data)
if serializer.is_valid():
    print('Valid - This should NOT happen!')
else:
    print('Validation Errors (Expected):')
    print(serializer.errors)

print('\n' + '='*50 + '\n')

# Test validation for valid publication year
data2 = {
    'title': 'Valid Book',
    'publication_year': 2020,
    'author': author.id
}

serializer2 = BookSerializer(data=data2)
if serializer2.is_valid():
    print('Valid - Publication year 2020 is acceptable!')
    book = serializer2.save()
    print(f'Created book: {book}')
else:
    print('Validation Errors (Should NOT happen):')
    print(serializer2.errors)
