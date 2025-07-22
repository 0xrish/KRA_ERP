# 🚆 ICF Forms API Documentation

**✅ Backend Integration**: This Flutter frontend is properly connected with the `@/Backend` directory, providing seamless API integration with the Django backend for all form submissions and data management.

This project handles digital form submissions for:

1. ✅ ICF Wheel Specifications Form  
2. ✅ ICF Bogie Checksheet Form

Both forms are digitally captured, submitted, and queried via REST APIs.

---

## 🔗 How Backend is Properly Connected

### 🏗️ Architecture Overview

The Flutter frontend integrates seamlessly with the Django backend located in `@/Backend` through a well-structured API service layer:

```
Flutter App (Frontend)     ←→     Django API (Backend)
├── UI Screens             ←→     ├── Django Ninja APIs
├── Provider State         ←→     ├── Pydantic Schemas
├── Service Layer          ←→     ├── Database Models
├── Model Classes          ←→     ├── JWT Authentication
└── Local Storage          ←→     └── PostgreSQL Database
```

### 🔧 Connection Implementation

#### 1. **API Service Layer Structure**

```dart
lib/
├── services/
│   ├── api_services/
│   │   ├── base_api_service.dart    # Core HTTP client
│   │   ├── auth_service.dart        # Authentication APIs
│   │   └── form_service.dart        # Form submission APIs
│   ├── authentication_services/
│   │   ├── login_service.dart       # Login/logout logic
│   │   └── token_manager.dart       # JWT token management
│   └── form_services/
│       ├── wheel_spec_service.dart  # Wheel form APIs
│       └── bogie_service.dart       # Bogie form APIs
```

#### 2. **Base API Configuration**

```dart
// lib/services/api_services/base_api_service.dart
class BaseApiService {
  static const String baseUrl = 'http://localhost:8000';  // Development
  static const String apiPrefix = '/api';
  
  // Production: 'https://your-domain.com'
  // Configure based on environment
}
```

#### 3. **Authentication Flow Integration**

```dart
// JWT Token Management
class AuthService {
  // Login to Django backend
  Future<AuthResponse> login(String phoneNumber, String password) async {
    final response = await http.post(
      Uri.parse('${BaseApiService.baseUrl}/api/users/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'phone_number': phoneNumber,
        'password': password,
      }),
    );
    // Handle JWT tokens from Django response
  }
  
  // Auto-refresh tokens
  Future<void> refreshToken() async {
    // Calls Django's /api/users/refresh endpoint
  }
}
```

#### 4. **Form Submission Integration**

```dart
// lib/services/form_services/wheel_spec_service.dart
class WheelSpecService {
  Future<ApiResponse> submitWheelForm(WheelSpecModel wheelData) async {
    final token = await TokenManager.getAccessToken();
    
    final response = await http.post(
      Uri.parse('${BaseApiService.baseUrl}/api/forms/wheel-specifications'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode(wheelData.toJson()),
    );
    
    return ApiResponse.fromJson(response);
  }
}
```

### 🔐 Authentication Integration

#### JWT Token Management
- **Storage**: Tokens stored securely in `SharedPreferences`
- **Auto-refresh**: Automatic token refresh before expiration
- **Security**: Proper token validation and logout on failure

```dart
// Token flow with Django backend
1. User logs in → Flutter sends credentials to Django
2. Django validates → Returns JWT access + refresh tokens
3. Flutter stores tokens → Uses in all subsequent API calls
4. Token expires → Flutter auto-refreshes using Django's refresh endpoint
5. Refresh fails → User redirected to login screen
```

### 📊 Data Flow Integration

#### 1. **Form Submission Flow**
```
User Input → Validation → API Call → Django Processing → Database → Response → UI Update
```

#### 2. **State Management with Backend**
```dart
// Using Provider pattern with backend integration
class FormProvider extends ChangeNotifier {
  final FormService _formService = FormService();
  
  Future<void> submitForm(FormData data) async {
    setLoading(true);
    try {
      final response = await _formService.submitForm(data);
      if (response.success) {
        setSuccess(response.message);
      } else {
        setError(response.error);
      }
    } catch (e) {
      setError('Connection error: ${e.toString()}');
    } finally {
      setLoading(false);
    }
  }
}
```

### 🛠️ Backend API Endpoints Used

| Flutter Service | Django Endpoint | Purpose |
|----------------|-----------------|---------|
| `AuthService.login()` | `POST /api/users/login` | User authentication |
| `AuthService.register()` | `POST /api/users/register` | User registration |
| `AuthService.refreshToken()` | `POST /api/users/refresh` | Token refresh |
| `FormService.submitWheelForm()` | `POST /api/forms/wheel-specifications` | Submit wheel form |
| `FormService.submitBogieForm()` | `POST /api/forms/bogie-checksheet` | Submit bogie form |
| `FormService.getForms()` | `GET /api/forms/wheel-specifications` | Retrieve forms |
| `UserService.getProfile()` | `GET /api/users/profile` | Get user data |

### 🔧 Error Handling & Connectivity

#### Network Error Handling
```dart
class ApiErrorHandler {
  static void handleError(http.Response response) {
    switch (response.statusCode) {
      case 401:
        // Token expired - refresh or redirect to login
        AuthService.refreshTokenOrLogout();
        break;
      case 403:
        // Unauthorized - show permission error
        break;
      case 500:
        // Server error - show backend error message
        break;
      default:
        // Handle other errors
    }
  }
}
```

#### Connection Verification
```dart
class ConnectionChecker {
  static Future<bool> checkBackendConnection() async {
    try {
      final response = await http.get(
        Uri.parse('${BaseApiService.baseUrl}/api/health/'),
        timeout: Duration(seconds: 5),
      );
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}
```

### 🚀 Development Setup for Backend Integration

#### 1. **Configure Backend URL**
```dart
// lib/config/api_config.dart
class ApiConfig {
  static const String development = 'http://localhost:8000';
  static const String production = 'https://your-production-domain.com';
  
  static String get baseUrl {
    return kDebugMode ? development : production;
  }
}
```

#### 2. **Test Backend Connection**
```bash
# Ensure Django backend is running
cd @/Backend
python manage.py runserver

# Test API endpoints
curl http://localhost:8000/api/docs/  # Should show Swagger UI
```

#### 3. **Flutter Dependencies for Backend Integration**
```yaml
# pubspec.yaml
dependencies:
  http: ^1.1.0           # HTTP client for API calls
  shared_preferences: ^2.2.2  # Token storage
  provider: ^6.1.2       # State management
  json_annotation: ^4.8.1     # JSON serialization
```

### 📱 Platform-Specific Backend Integration

#### Android
- Network security config for HTTP in development
- Certificate pinning for production

#### iOS  
- App Transport Security settings
- Proper network permissions

#### Web
- CORS handling with Django backend
- Cookie-based session management option

### 🔍 Testing Backend Integration

```dart
// test/integration/backend_integration_test.dart
void main() {
  group('Backend Integration Tests', () {
    test('should connect to Django backend', () async {
      final isConnected = await ConnectionChecker.checkBackendConnection();
      expect(isConnected, true);
    });
    
    test('should authenticate with backend', () async {
      final authService = AuthService();
      final response = await authService.login('+1234567890', 'password');
      expect(response.success, true);
      expect(response.accessToken, isNotNull);
    });
  });
}
```

---

## 📌 TODOs / In-Scope Features

- [x] Submit Wheel Specifications form
- [x] Submit Bogie Checksheet form (multi-section)
- [x] Search both forms by Form Number / Inspector / Date
- [x] Dropdown support for "Inspection By" (from DB)
- [ ] Admin dashboard to view all forms
- [ ] Edit/Delete forms (Admin only)
- [ ] Export forms as PDF (optional)
- [ ] Authentication & role-based access (optional)

---

## 📘 1. Wheel Specifications Form

### 📤 API: `POST /api/forms/wheel-specifications`

**Description:** Submit ICF wheel specification form

#### Payload:
```json
{
  "formNumber": "WHEEL-2025-001",
  "submittedBy": "user_id_123",
  "submittedDate": "2025-07-03",
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


2. POST /api/forms/bogie-checksheet


{
  "formNumber": "BOGIE-2025-001",
  "inspectionBy": "user_id_456",
  "inspectionDate": "2025-07-03",
  "bogieDetails": {
    "bogieNo": "BG1234",
    "makerYearBuilt": "RDSO/2018",
    "incomingDivAndDate": "NR / 2025-06-25",
    "deficitComponents": "None",
    "dateOfIOH": "2025-07-01"
  },
  "bogieChecksheet": {
    "bogieFrameCondition": "Good",
    "bolster": "Good",
    "bolsterSuspensionBracket": "Cracked",
    "lowerSpringSeat": "Good",
    "axleGuide": "Worn",
    ...
  },
  "bmbcChecksheet": {
    "cylinderBody": "WORN OUT",
    "pistonTrunnion": "GOOD",
    "adjustingTube": "DAMAGED",
    "plungerSpring": "GOOD",
    ...
  }
}
  

  
