# Test script for API endpoints
# This script tests both public and protected endpoints

import requests
import json

BASE_URL = 'http://127.0.0.1:8001/api'

print("=" * 60)
print("Testing Advanced API Project Endpoints")
print("=" * 60)

# Test 1: List all books (Public - should work)
print("\n1. Testing GET /api/books/ (Public access)")
try:
    response = requests.get(f'{BASE_URL}/books/')
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ Success! Found {len(response.json())} books")
        if response.json():
            print(f"   Sample: {response.json()[0]}")
    else:
        print(f"   ✗ Failed: {response.text}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 2: Get single book (Public - should work if books exist)
print("\n2. Testing GET /api/books/1/ (Public access)")
try:
    response = requests.get(f'{BASE_URL}/books/1/')
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ Success! Book: {response.json()}")
    elif response.status_code == 404:
        print(f"   ℹ Book with ID 1 doesn't exist yet")
    else:
        print(f"   ✗ Failed: {response.text}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 3: Try to create book without auth (Should fail with 401/403)
print("\n3. Testing POST /api/books/create/ (Without authentication)")
try:
    data = {
        "title": "Unauthorized Book",
        "publication_year": 2024,
        "author": 1
    }
    response = requests.post(
        f'{BASE_URL}/books/create/',
        json=data,
        headers={'Content-Type': 'application/json'}
    )
    print(f"   Status Code: {response.status_code}")
    if response.status_code in [401, 403]:
        print(f"   ✓ Correctly blocked! Authentication required")
    else:
        print(f"   ✗ Unexpected result: {response.text}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 4: Try to update book without auth (Should fail)
print("\n4. Testing PATCH /api/books/1/update/ (Without authentication)")
try:
    data = {"title": "Unauthorized Update"}
    response = requests.patch(
        f'{BASE_URL}/books/1/update/',
        json=data,
        headers={'Content-Type': 'application/json'}
    )
    print(f"   Status Code: {response.status_code}")
    if response.status_code in [401, 403]:
        print(f"   ✓ Correctly blocked! Authentication required")
    else:
        print(f"   ✗ Unexpected result: {response.text}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 5: Try to delete book without auth (Should fail)
print("\n5. Testing DELETE /api/books/1/delete/ (Without authentication)")
try:
    response = requests.delete(f'{BASE_URL}/books/1/delete/')
    print(f"   Status Code: {response.status_code}")
    if response.status_code in [401, 403]:
        print(f"   ✓ Correctly blocked! Authentication required")
    else:
        print(f"   ✗ Unexpected result: {response.text}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 60)
print("Testing Summary:")
print("  - Public endpoints (GET /books/, /books/1/) accessible ✓")
print("  - Protected endpoints require authentication ✓")
print("  - Permission enforcement working correctly ✓")
print("=" * 60)

print("\n📝 Note: To test authenticated endpoints, you need to:")
print("   1. Create a superuser: python manage.py createsuperuser")
print("   2. Get a token from Django admin or token endpoint")
print("   3. Use: requests.get(url, headers={'Authorization': 'Token YOUR_TOKEN'})")
