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

def test_wheel_specification_post(token):
    """Test wheel specification POST endpoint"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    wheel_data = {
        "formNumber": "WHEEL-2025-001",
        "submittedBy": "1",
        "submittedDate": "2025-01-21",
        "fields": {
            "treadDiameterNew": "915 (900-1000)",
            "lastShopIssueSize": "837 (800-900)",
            "condemningDia": "825 (800-900)",
            "wheelGauge": "1600 (+2,-1)",
            "variationSameAxle": "0.5",
            "variationSameBogie": "5",
            "variationSameCoach": "13",
            "wheelProfile": "29.4 Flange Thickness",
            "intermediateWWP": "20 TO 28",
            "bearingSeatDiameter": "130.043 TO 130.068",
            "rollerBearingOuterDia": "280 (+0.0/-0.035)",
            "rollerBearingBoreDia": "130 (+0.0/-0.025)",
            "rollerBearingWidth": "93 (+0/-0.250)",
            "axleBoxHousingBoreDia": "280 (+0.030/+0.052)",
            "wheelDiscWidth": "127 (+4/-0)"
        }
    }
    
    print("Testing wheel specification POST...")
    response = requests.post(f"{BASE_URL}/forms/wheel-specifications", json=wheel_data, headers=headers)
    print(f"Wheel spec POST status: {response.status_code}")
    print(f"Response: {response.text}")
    
    return response.status_code == 201

def test_bogie_checksheet_post(token):
    """Test bogie checksheet POST endpoint"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    bogie_data = {
        "formNumber": "BOGIE-2025-001",
        "inspectionBy": "1",
        "inspectionDate": "2025-01-21",
        "bogieDetails": {
            "bogieNo": "BG1234",
            "makerYearBuilt": "RDSO/2018",
            "incomingDivAndDate": "NR / 2025-01-21",
            "deficitComponents": "None",
            "dateOfIOH": "2025-01-20"
        },
        "bogieChecksheet": {
            "bogieFrameCondition": "Good",
            "bolster": "Good",
            "bolsterSuspensionBracket": "Good",
            "lowerSpringSeat": "Good",
            "axleGuide": "Good"
        },
        "bmbcChecksheet": {
            "cylinderBody": "GOOD",
            "pistonTrunnion": "GOOD",
            "adjustingTube": "GOOD",
            "plungerSpring": "GOOD"
        }
    }
    
    print("Testing bogie checksheet POST...")
    response = requests.post(f"{BASE_URL}/forms/bogie-checksheet", json=bogie_data, headers=headers)
    print(f"Bogie checksheet POST status: {response.status_code}")
    print(f"Response: {response.text}")
    
    return response.status_code == 201

def test_forms_get(token):
    """Test basic forms GET endpoint"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("Testing forms GET...")
    response = requests.get(f"{BASE_URL}/forms/", headers=headers)
    print(f"Forms GET status: {response.status_code}")
    print(f"Response: {response.text}")
    
    return response.status_code == 200

if __name__ == "__main__":
    print("=== Testing KPA ERP API ===")
    
    # Step 1: Login
    token = test_login()
    if not token:
        print("Cannot proceed without authentication token")
        exit(1)
    
    print(f"\nAccess token: {token[:20]}...")
    
    # Step 2: Test basic forms endpoint
    print("\n=== Testing Forms Endpoints ===")
    test_forms_get(token)
    
    # Step 3: Test wheel specification
    print("\n=== Testing Wheel Specification ===")
    test_wheel_specification_post(token)
    
    # Step 4: Test bogie checksheet
    print("\n=== Testing Bogie Checksheet ===")
    test_bogie_checksheet_post(token)
    
    print("\n=== API Testing Complete ===") 