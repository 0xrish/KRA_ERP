import requests
import json

# Base URL
BASE_URL = "http://localhost:8000/api"

def test_login():
    """Test user login"""
    login_data = {
        "phone_number": "9325229203",
        "password": "@Rishi21"
    }
    
    response = requests.post(f"{BASE_URL}/users/login", json=login_data)
    print(f"Login status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("Login successful!")
        return result["access_token"]
    else:
        print(f"Login failed: {response.text}")
        return None

def get_openapi_schema():
    """Get the OpenAPI schema to see available endpoints"""
    try:
        response = requests.get(f"{BASE_URL}/openapi.json")
        if response.status_code == 200:
            schema = response.json()
            print("Available API endpoints:")
            for path, methods in schema.get('paths', {}).items():
                for method in methods.keys():
                    print(f"  {method.upper()} {path}")
        else:
            print(f"Failed to get OpenAPI schema: {response.status_code}")
    except Exception as e:
        print(f"Error getting OpenAPI schema: {e}")

def test_endpoint_methods(token):
    """Test different HTTP methods on the forms endpoints"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    endpoints_to_test = [
        "/forms/wheel-specifications",
        "/forms/bogie-checksheet",
        "/forms/",
    ]
    
    methods = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    
    for endpoint in endpoints_to_test:
        print(f"\nTesting endpoint: {endpoint}")
        for method in methods:
            try:
                response = requests.request(method, f"{BASE_URL}{endpoint}", headers=headers, timeout=5)
                print(f"  {method}: {response.status_code}")
                if response.status_code == 405:
                    # Check what methods are allowed
                    allowed = response.headers.get('Allow', 'Not specified')
                    print(f"    Allowed methods: {allowed}")
            except Exception as e:
                print(f"  {method}: Error - {e}")

def test_direct_url():
    """Test accessing URLs directly to check routing"""
    test_urls = [
        "http://localhost:8000/api/users/",
    ]
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=5)
            print(f"{url}: {response.status_code}")
        except Exception as e:
            print(f"{url}: Error - {e}")


def test_form_submission_api(token):
    """Test the new form submission endpoint"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("\n=== Testing Form Submission API ===")
    
    # First, let's get available forms
    print("1. Getting available forms...")
    try:
        response = requests.get(f"{BASE_URL}/forms/", headers=headers)
        print(f"   Forms list status: {response.status_code}")
        
        if response.status_code == 200:
            forms = response.json()
            print(f"   Found {len(forms)} forms")
            if forms:
                form = forms[0]  # Use first form for testing
                form_id = form['id']
                form_title = form['title']
                print(f"   Using form: {form_title} (ID: {form_id})")
                
                # Test form submission
                print("\n2. Testing form submission...")
                submission_data = {
                    "form_id": form_id,
                    "submission_data": {
                        "name": "Test User",
                        "email": "test@example.com",
                        "message": "This is a test submission from the debug script",
                        "test_field": "API test value"
                    },
                    "notes": "Test submission created by debug script"
                }
                
                response = requests.post(f"{BASE_URL}/forms/submissions", json=submission_data, headers=headers)
                print(f"   Submission status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print("   ✅ Form submission successful!")
                    print(f"   Submission ID: {result['id']}")
                    print(f"   Form: {result['form_title']}")
                    print(f"   Status: {result['status']}")
                    print(f"   Submitted at: {result['submitted_at']}")
                    
                    # Test getting submissions list
                    print("\n3. Testing submissions list...")
                    response = requests.get(f"{BASE_URL}/forms/submissions", headers=headers)
                    print(f"   Submissions list status: {response.status_code}")
                    
                    if response.status_code == 200:
                        submissions = response.json()
                        print(f"   Found {len(submissions)} submissions")
                        print("   ✅ Submissions list working!")
                        
                        # Test filtering by form_id
                        print("\n4. Testing filtered submissions...")
                        response = requests.get(f"{BASE_URL}/forms/submissions?form_id={form_id}", headers=headers)
                        print(f"   Filtered submissions status: {response.status_code}")
                        
                        if response.status_code == 200:
                            filtered_submissions = response.json()
                            print(f"   Found {len(filtered_submissions)} submissions for form {form_id}")
                            print("   ✅ Submission filtering working!")
                        else:
                            print(f"   ❌ Submission filtering failed: {response.text}")
                    else:
                        print(f"   ❌ Submissions list failed: {response.text}")
                else:
                    print(f"   ❌ Form submission failed: {response.text}")
                    print(f"   Response: {response.json() if response.headers.get('content-type') == 'application/json' else response.text}")
            else:
                print("   No forms available for testing. Creating a test form...")
                
                # Create a test form
                form_data = {
                    "title": "Test Form for API",
                    "description": "A test form created by the debug script",
                    "form_type": "other",
                    "is_active": True
                }
                
                response = requests.post(f"{BASE_URL}/forms/", json=form_data, headers=headers)
                print(f"   Form creation status: {response.status_code}")
                
                if response.status_code == 200:
                    new_form = response.json()
                    print(f"   ✅ Created test form: {new_form['title']} (ID: {new_form['id']})")
                    # Recursively call this function to test with the new form
                    test_form_submission_api(token)
                else:
                    print(f"   ❌ Form creation failed: {response.text}")
        else:
            print(f"   ❌ Failed to get forms: {response.text}")
    except Exception as e:
        print(f"   ❌ Error testing form submission API: {e}")

if __name__ == "__main__":
    print("=== Debugging KPA ERP API ===")
    
    # Test server connectivity
    print("\n=== Testing Server Connectivity ===")
    test_direct_url()
    
    # Get OpenAPI schema
    print("\n=== Getting OpenAPI Schema ===")
    get_openapi_schema()
    
    # Login
    print("\n=== Testing Login ===")
    token = test_login()
    
    if token:
        # Test endpoint methods
        print("\n=== Testing Endpoint Methods ===")
        test_endpoint_methods(token)

        # Test form submission API
        print("\n=== Testing Form Submission API ===")
        test_form_submission_api(token)
    
    print("\n=== Debug Complete ===") 