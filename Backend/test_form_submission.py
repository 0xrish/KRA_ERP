#!/usr/bin/env python3
"""
Simple test script for the form submission API endpoint
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000/api"

def test_form_submission():
    """Test the form submission endpoint step by step"""
    
    # Step 1: Login to get token
    print("Step 1: Logging in...")
    login_data = {
        "phone_number": "9325229203",
        "password": "@Rishi21"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/login", json=login_data)
        if response.status_code != 200:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return False
        
        token = response.json()["access_token"]
        print("✅ Login successful")
        
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Step 2: Check available forms
    print("\nStep 2: Getting available forms...")
    try:
        response = requests.get(f"{BASE_URL}/forms/", headers=headers)
        print(f"Forms list response: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Failed to get forms: {response.text}")
            return False
            
        forms = response.json()
        print(f"✅ Found {len(forms)} forms")
        
        # Create a form if none exist
        if not forms:
            print("Creating a test form...")
            form_data = {
                "title": "Test Submission Form",
                "description": "A form for testing submissions",
                "form_type": "other",
                "is_active": True
            }
            
            response = requests.post(f"{BASE_URL}/forms/", json=form_data, headers=headers)
            if response.status_code != 200:
                print(f"❌ Failed to create form: {response.text}")
                return False
                
            new_form = response.json()
            form_id = new_form['id']
            print(f"✅ Created test form with ID: {form_id}")
        else:
            form_id = forms[0]['id']
            print(f"✅ Using existing form with ID: {form_id}")
            
    except Exception as e:
        print(f"❌ Error getting forms: {e}")
        return False
    
    # Step 3: Test the submissions endpoint directly
    print(f"\nStep 3: Testing submissions endpoint...")
    
    # First test if the endpoint exists with OPTIONS
    try:
        response = requests.options(f"{BASE_URL}/forms/submissions", headers=headers)
        print(f"OPTIONS response: {response.status_code}")
        if 'Allow' in response.headers:
            print(f"Allowed methods: {response.headers['Allow']}")
    except Exception as e:
        print(f"OPTIONS error: {e}")
    
    # Test GET method
    try:
        response = requests.get(f"{BASE_URL}/forms/submissions", headers=headers)
        print(f"GET submissions response: {response.status_code}")
        if response.status_code == 200:
            submissions = response.json()
            print(f"✅ GET working - found {len(submissions)} submissions")
        else:
            print(f"GET failed: {response.text}")
    except Exception as e:
        print(f"GET error: {e}")
    
    # Test POST method
    print(f"\nStep 4: Testing POST submission...")
    submission_data = {
        "form_id": form_id,
        "submission_data": {
            "name": "Test User",
            "email": "test@example.com",
            "message": "Test submission from focused test script"
        },
        "notes": "Created by test script"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/forms/submissions", json=submission_data, headers=headers)
        print(f"POST submission response: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Form submission successful!")
            print(f"   Submission ID: {result['id']}")
            print(f"   Form: {result['form_title']}")
            print(f"   Status: {result['status']}")
            return True
        else:
            print(f"❌ POST failed: {response.text}")
            # Try to get more details
            try:
                error_detail = response.json()
                print(f"Error details: {json.dumps(error_detail, indent=2)}")
            except:
                pass
            return False
            
    except Exception as e:
        print(f"❌ POST error: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing Form Submission API ===")
    success = test_form_submission()
    
    if success:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Tests failed!")
        sys.exit(1) 