# KPA ERP System - Complete Features Documentation

**Version:** 1.0.0  
**Technology Stack:** Django 5.2.4 + Django Ninja + PostgreSQL + JWT Authentication  
**Target Industry:** Railway Maintenance & Operations  

---

## 🎯 Executive Summary

The KPA ERP System is a modern, enterprise-grade API-first application designed specifically for railway maintenance operations. Built with Django Ninja for high-performance REST APIs, it features phone-based authentication, specialized forms for wheel and bogie maintenance, and comprehensive user management with role-based access control.

---

## 🏗️ System Architecture

### Core Technology Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **Backend Framework** | Django | 5.2.4 | Core application framework |
| **API Framework** | Django Ninja | 1.4.3 | Fast, modern REST API with OpenAPI |
| **Database** | PostgreSQL | 13+ | Primary data store with ACID compliance |
| **Authentication** | JWT (PyJWT) | 2.10.1 | Stateless token-based authentication |
| **Data Validation** | Pydantic | 2.11.7 | Type-safe data validation and serialization |
| **Containerization** | Docker & Docker Compose | Latest | Development and production deployment |
| **Web Server** | Nginx + Gunicorn | Production | Reverse proxy and WSGI server |
| **Caching** | Redis | 7.0 | Session management and performance optimization |

### Application Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    KPA ERP System                           │
├─────────────────────────────────────────────────────────────┤
│  API Layer (Django Ninja)                                  │
│  ├── Authentication API     ├── Forms API                  │
│  ├── User Management API    ├── Maintenance Forms API      │
│  └── Auto-generated OpenAPI Documentation                  │
├─────────────────────────────────────────────────────────────┤
│  Business Logic Layer                                      │
│  ├── Custom User Model      ├── Form Validation           │
│  ├── JWT Token Management   ├── Maintenance Workflows     │
│  └── Permission System      └── Data Processing           │
├─────────────────────────────────────────────────────────────┤
│  Data Access Layer                                         │
│  ├── PostgreSQL Database    ├── Redis Cache               │
│  ├── Django ORM Models      ├── File Storage              │
│  └── Database Indexes       └── Session Management        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔐 Authentication & Security Features

### 1. Phone-Based Authentication System

**Innovation:** Unlike traditional email-based systems, KPA ERP uses phone numbers as the primary authentication identifier, optimized for field workers and operations teams.

#### Features:
- **Custom User Model** with phone number as USERNAME_FIELD
- **International Phone Number Support** with regex validation (`^\+?1?\d{9,15}$`)
- **JWT Token Authentication** with configurable expiration
- **Refresh Token Rotation** for enhanced security
- **Phone Number Validation** with format enforcement

#### Implementation Details:
```python
# Custom User Model Features
- Phone number as primary identifier (unique)
- Optional email field for notifications
- Comprehensive profile fields (address, business info)
- Manager hierarchy support (self-referencing relationship)
- Employee ID integration for HR systems
```

#### API Endpoints:
- `POST /api/users/register` - Create new user account
- `POST /api/users/login` - Authenticate with phone/password
- `POST /api/users/refresh` - Refresh access tokens
- `POST /api/users/change-password` - Secure password updates

### 2. JWT Security Implementation

#### Token Configuration:
- **Access Token Lifetime:** 1 hour (configurable)
- **Refresh Token Lifetime:** 7 days with rotation
- **Algorithm:** HS256 with secure signing key
- **Blacklist Support:** Prevents reuse of rotated tokens
- **Automatic Last Login Updates:** Audit trail maintenance

#### Security Headers:
```http
Authorization: Bearer <access_token>
Content-Type: application/json
X-Requested-With: XMLHttpRequest
```

---

## 👥 User Management System

### 1. Comprehensive User Profiles

#### User Data Model:
```python
# Personal Information
- first_name, last_name (required)
- phone_number (unique identifier)
- email (optional, for notifications)
- profile_picture (image upload)
- bio (up to 500 characters)
- date_of_birth

# Address Information
- address_line_1, address_line_2
- city, state, postal_code, country
- Full address property for concatenated display

# Business Information
- employee_id (unique, for payroll integration)
- department, position
- manager (hierarchical relationships)
- Staff status (admin privileges)
```

### 2. Role-Based Access Control

#### User Roles:
- **Regular Users:** Profile management, form submissions
- **Staff Users:** Admin access, user management, form oversight
- **Superusers:** Full system administration

#### Permission Matrix:
| Action | Regular User | Staff User | Superuser |
|--------|-------------|------------|-----------|
| View own profile | ✅ | ✅ | ✅ |
| Update own profile | ✅ | ✅ | ✅ |
| View all users | ❌ | ✅ | ✅ |
| Create users | ❌ | ✅ | ✅ |
| Deactivate users | ❌ | ✅ | ✅ |
| Submit forms | ✅ | ✅ | ✅ |
| Review submissions | ❌ | ✅ | ✅ |
| System administration | ❌ | ❌ | ✅ |

### 3. User Management API

#### Administrative Functions:
- `GET /api/users/users` - List all users (admin only)
- `GET /api/users/users/{id}` - Get user details
- `POST /api/users/users` - Create new user (admin only)
- `PUT /api/users/users/{id}` - Update user profile
- `DELETE /api/users/users/{id}` - Deactivate user (soft delete)

---

## 📋 Dynamic Forms System

### 1. Generic Form Builder

#### Form Model Features:
```python
# Form Template
- title, description
- form_type (contact, feedback, survey, application, other)
- is_active (enable/disable forms)
- created_by (audit trail)
- timestamps (created_at, updated_at)

# Form Fields
- 13 field types supported
- Custom validation rules (JSON)
- Field ordering system
- Help text and placeholders
- Required field enforcement
```

#### Supported Field Types:
1. **Text Input:** Single-line text
2. **Email:** Email validation
3. **Number:** Numeric input with validation
4. **Phone:** Phone number format
5. **URL:** URL validation
6. **Textarea:** Multi-line text
7. **Select:** Dropdown with options
8. **Radio:** Single choice from options
9. **Checkbox:** Multiple selections
10. **Date:** Date picker
11. **Time:** Time picker
12. **DateTime:** Combined date/time
13. **File:** File upload with validation

### 2. Form Submission System

#### Submission Workflow:
```python
# Submission States
- pending (initial state)
- reviewed (under review)
- approved (accepted)
- rejected (declined)

# Submission Data
- JSON storage for flexible data
- User attribution (submitted_by)
- Review tracking (reviewed_by, reviewed_at)
- Notes and comments system
```

---

## 🚂 Specialized Railway Maintenance Forms

### 1. Wheel Specification Management

**Purpose:** Detailed tracking of wheel measurements and specifications for railway maintenance operations.

#### Key Features:
- **Unique Form Numbers:** Automatic validation and conflict prevention
- **17 Measurement Fields:** Comprehensive wheel dimension tracking
- **Tolerance Specifications:** Range validation for engineering standards
- **Status Workflow:** saved → submitted → reviewed → approved/rejected
- **Database Optimization:** Indexed fields for fast queries

#### Measurement Categories:

##### Dimensional Measurements:
- **Tread Diameter (New):** 915mm (900-1000mm range)
- **Last Shop Issue Size:** 837mm (800-900mm range)
- **Condemning Diameter:** 825mm (800-900mm range)
- **Wheel Gauge:** 1600mm (+2,-1 tolerance)

##### Variation Measurements:
- **Same Axle Variation:** 0.5mm tolerance
- **Same Bogie Variation:** 5mm tolerance
- **Same Coach Variation:** 13mm tolerance

##### Profile & Bearing Specifications:
- **Wheel Profile:** 29.4mm Flange Thickness
- **Intermediate WWP:** 20-28mm range
- **Bearing Seat Diameter:** 130.043-130.068mm
- **Roller Bearing Specifications:** Outer diameter, bore, width
- **Axle Box Housing:** Bore diameter specifications
- **Wheel Disc Width:** 127mm (+4/-0 tolerance)

#### API Integration:
```json
POST /api/forms/wheel-specifications
{
  "formNumber": "WS-2024-001",
  "submittedBy": "user_id",
  "submittedDate": "2024-01-15",
  "fields": {
    "treadDiameterNew": "915 (900-1000)",
    "lastShopIssueSize": "837 (800-900)",
    // ... all 15 measurement fields
  }
}
```

### 2. Bogie Checksheet System

**Purpose:** Comprehensive inspection forms for bogie components and BMBC (Brake Monitoring and Control) systems.

#### Inspection Categories:

##### Bogie Details Section:
- **Bogie Number:** Unique identifier
- **Maker/Year Built:** Manufacturing information
- **Incoming Division & Date:** Transfer tracking
- **Deficit Components:** Missing parts inventory
- **Date of IOH:** Last major overhaul

##### Bogie Component Conditions:
- **Bogie Frame:** Structural integrity assessment
- **Bolster:** Load-bearing component status
- **Bolster Suspension Bracket:** Critical safety component
- **Lower Spring Seat:** Suspension system component
- **Axle Guide:** Wheel alignment component

##### BMBC Component Assessment:
- **Cylinder Body:** Brake system component
- **Piston Trunnion:** Brake mechanism part
- **Adjusting Tube:** Brake adjustment component
- **Plunger Spring:** Brake spring mechanism

#### Condition Rating System:
- **GOOD:** Component in excellent condition
- **FAIR:** Component functional with minor wear
- **POOR/WORN OUT:** Component needs attention
- **DAMAGED/CRACKED:** Component requires immediate replacement

#### API Structure:
```json
POST /api/forms/bogie-checksheets
{
  "formNumber": "BC-2024-001",
  "inspectionBy": "inspector_id",
  "inspectionDate": "2024-01-15",
  "bogieDetails": {
    "bogieNo": "B-12345",
    "makerYearBuilt": "ICF/2020",
    // ... bogie metadata
  },
  "bogieChecksheet": {
    "bogieFrameCondition": "Good",
    // ... component conditions
  },
  "bmbcChecksheet": {
    "cylinderBody": "GOOD",
    // ... BMBC component conditions
  }
}
```

---

## 🔗 API Framework & Documentation

### 1. Django Ninja Implementation

#### Performance Advantages:
- **3-5x Faster** than Django REST Framework
- **Async Support:** Full async/await compatibility
- **Pydantic Integration:** Type-safe validation
- **Automatic OpenAPI:** Zero-config documentation
- **Intuitive API:** FastAPI-inspired design

#### API Design Principles:
- **RESTful Routes:** Consistent URL patterns
- **HTTP Status Codes:** Proper response codes
- **Error Handling:** Structured error responses
- **Content Negotiation:** JSON by default
- **CORS Support:** Cross-origin request handling

### 2. Auto-Generated Documentation

#### Interactive Documentation:
- **Swagger UI:** Available at `/api/docs/`
- **ReDoc:** Alternative documentation view
- **OpenAPI 3.0 Schema:** Machine-readable specification
- **Try-it-out Feature:** Live API testing
- **Authentication Integration:** JWT token testing

#### Documentation Features:
- **Endpoint Descriptions:** Detailed operation explanations
- **Request/Response Examples:** Real-world usage samples
- **Schema Definitions:** Data model specifications
- **Error Code Documentation:** Complete error reference
- **Authentication Guide:** Token usage instructions

### 3. API Endpoint Summary

#### Authentication Endpoints:
```
POST   /api/users/register      # User registration
POST   /api/users/login         # User authentication
POST   /api/users/refresh       # Token refresh
```

#### User Management:
```
GET    /api/users/profile       # Current user profile
PUT    /api/users/profile       # Update profile
POST   /api/users/change-password # Password change
GET    /api/users/users         # List users (admin)
POST   /api/users/users         # Create user (admin)
GET    /api/users/users/{id}    # Get user details
PUT    /api/users/users/{id}    # Update user
DELETE /api/users/users/{id}    # Deactivate user
```

#### Forms Management:
```
POST   /api/forms/wheel-specifications    # Create wheel spec
GET    /api/forms/wheel-specifications    # List wheel specs
POST   /api/forms/bogie-checksheets       # Create bogie checksheet
GET    /api/forms/bogie-checksheets       # List bogie checksheets
```

---

## 🗄️ Database Design & Optimization

### 1. PostgreSQL Implementation

#### Database Features:
- **ACID Compliance:** Transaction integrity
- **JSON Support:** Flexible data storage
- **Full-text Search:** Advanced query capabilities
- **Indexing Strategy:** Optimized query performance
- **Connection Pooling:** Scalable connection management

#### Schema Organization:
```sql
-- Core Tables
users                    # Custom user model
forms                    # Form templates
form_fields             # Dynamic form fields
form_submissions        # Generic submissions

-- Specialized Tables
wheel_specifications    # Wheel maintenance data
bogie_checksheets      # Bogie inspection data
```

### 2. Database Indexing Strategy

#### Performance Indexes:
```sql
-- User table indexes
CREATE INDEX idx_users_phone_number ON users(phone_number);
CREATE INDEX idx_users_employee_id ON users(employee_id);
CREATE INDEX idx_users_is_active ON users(is_active);

-- Wheel specifications indexes
CREATE INDEX idx_wheel_spec_form_number ON wheel_specifications(form_number);
CREATE INDEX idx_wheel_spec_submitted_by ON wheel_specifications(submitted_by);
CREATE INDEX idx_wheel_spec_date ON wheel_specifications(submitted_date);
CREATE INDEX idx_wheel_spec_status ON wheel_specifications(status);

-- Bogie checksheets indexes
CREATE INDEX idx_bogie_form_number ON bogie_checksheets(form_number);
CREATE INDEX idx_bogie_inspection_by ON bogie_checksheets(inspection_by);
CREATE INDEX idx_bogie_date ON bogie_checksheets(inspection_date);
CREATE INDEX idx_bogie_number ON bogie_checksheets(bogie_no);
```

### 3. Data Validation & Integrity

#### Model-Level Validation:
- **Phone Number Regex:** International format validation
- **Unique Constraints:** Preventing duplicates
- **Foreign Key Constraints:** Referential integrity
- **JSON Field Validation:** Pydantic schema enforcement
- **Choice Field Validation:** Enumerated value constraints

---

## 🐳 Infrastructure & Deployment

### 1. Docker Implementation

#### Multi-Container Architecture:
```yaml
services:
  db:           # PostgreSQL 15 with persistent storage
  redis:        # Redis 7 for caching and sessions
  web:          # Django application server
  nginx:        # Reverse proxy and static file serving
```

#### Container Features:
- **Volume Persistence:** Data and media storage
- **Environment Configuration:** Settings management
- **Health Checks:** Service monitoring
- **Restart Policies:** High availability
- **Resource Limits:** Performance optimization

### 2. Production Configuration

#### Security Hardening:
- **SSL/TLS Termination:** Nginx with certificate management
- **Static File Serving:** Optimized asset delivery
- **Database Security:** Connection encryption
- **CORS Policy:** Cross-origin request control
- **Rate Limiting:** API abuse prevention

#### Performance Optimization:
- **Gunicorn Workers:** Multi-process serving
- **Static File Compression:** Reduced bandwidth
- **Database Connection Pooling:** Resource efficiency
- **Redis Caching:** Session and query caching
- **Media File Optimization:** Image processing

### 3. Environment Management

#### Configuration Layers:
```python
# Base settings (config/settings/base.py)
- Common configurations
- Database settings
- JWT configuration
- API settings

# Development settings (config/settings/dev.py)
- Debug mode enabled
- CORS allow all origins
- Console email backend
- Django extensions

# Production settings (config/settings/prod.py)
- Security hardening
- Static file optimization
- Logging configuration
- Cache settings
```

---

## 📊 Data Models & Relationships

### 1. User Management Schema

```mermaid
erDiagram
    User {
        int id PK
        string phone_number UK
        string email
        string first_name
        string last_name
        string employee_id UK
        string department
        string position
        int manager_id FK
        boolean is_staff
        boolean is_active
        datetime date_joined
    }
    
    User ||--o{ User : manages
```

### 2. Forms System Schema

```mermaid
erDiagram
    Form {
        int id PK
        string title
        text description
        string form_type
        boolean is_active
        int created_by FK
        datetime created_at
    }
    
    FormField {
        int id PK
        int form_id FK
        string label
        string field_type
        json options
        json validation_rules
        int order
    }
    
    FormSubmission {
        int id PK
        int form_id FK
        int submitted_by FK
        json submission_data
        string status
        datetime submitted_at
    }
    
    Form ||--o{ FormField : contains
    Form ||--o{ FormSubmission : receives
    User ||--o{ Form : creates
    User ||--o{ FormSubmission : submits
```

### 3. Maintenance Forms Schema

```mermaid
erDiagram
    WheelSpecification {
        int id PK
        string form_number UK
        int submitted_by FK
        date submitted_date
        string tread_diameter_new
        string wheel_gauge
        string bearing_seat_diameter
        string status
        datetime created_at
    }
    
    BogieChecksheet {
        int id PK
        string form_number UK
        int inspection_by FK
        date inspection_date
        string bogie_no
        string bogie_frame_condition
        string cylinder_body
        string status
        datetime created_at
    }
    
    User ||--o{ WheelSpecification : submits
    User ||--o{ BogieChecksheet : inspects
```

---

## 🔧 Advanced Features

### 1. API Filtering & Search

#### Wheel Specifications Filtering:
```http
GET /api/forms/wheel-specifications?form_number=WS-2024&submitted_by=123&submitted_date=2024-01-15
```

#### Bogie Checksheets Filtering:
```http
GET /api/forms/bogie-checksheets?bogie_no=B-12345&inspection_date=2024-01-15&status=submitted
```

### 2. Error Handling & Validation

#### Structured Error Responses:
```json
{
  "success": false,
  "message": "Validation failed",
  "errors": {
    "phone_number": ["Phone number already exists"],
    "form_number": ["This form number is already in use"]
  }
}
```

#### Validation Features:
- **Pydantic Schema Validation:** Type-safe data validation
- **Custom Validators:** Business rule enforcement
- **Field-Level Errors:** Specific error targeting
- **Internationalization:** Multi-language error messages

### 3. File Upload Management

#### Profile Pictures:
- **Image Validation:** File type and size restrictions
- **Storage Organization:** Structured directory layout
- **URL Generation:** Secure access URLs
- **Optimization:** Automatic image processing

#### Form Attachments:
- **Multiple File Types:** Document and image support
- **Virus Scanning:** Security validation
- **Storage Quotas:** User and system limits
- **Access Control:** Permission-based downloads

---

## 📈 Performance & Scalability

### 1. Database Performance

#### Query Optimization:
- **Select Related:** Reduce N+1 queries
- **Prefetch Related:** Efficient relationship loading
- **Database Indexes:** Fast lookup performance
- **Query Analysis:** Performance monitoring

#### Scaling Strategies:
- **Read Replicas:** Distribute read operations
- **Connection Pooling:** Efficient connection management
- **Query Caching:** Reduce database load
- **Pagination:** Large dataset handling

### 2. API Performance

#### Response Optimization:
- **Serialization Caching:** Reduce processing time
- **Compression:** Gzip response compression
- **HTTP Caching:** Browser and proxy caching
- **CDN Integration:** Global content distribution

#### Rate Limiting:
- **Per-User Limits:** Prevent API abuse
- **Endpoint-Specific Limits:** Resource protection
- **Burst Handling:** Traffic spike management
- **Grace Period:** Fair usage policies

---

## 🔒 Security Implementation

### 1. Authentication Security

#### Token Management:
- **Secure Storage:** HttpOnly cookies option
- **Token Rotation:** Automatic refresh rotation
- **Blacklist Management:** Revoked token tracking
- **Expiration Handling:** Automatic cleanup

#### Password Security:
- **bcrypt Hashing:** Industry-standard encryption
- **Salt Generation:** Unique per-password salts
- **Complexity Requirements:** Configurable validation
- **Breach Protection:** Known password checking

### 2. API Security

#### Input Validation:
- **SQL Injection Prevention:** Parameterized queries
- **XSS Protection:** Input sanitization
- **CSRF Protection:** Token-based validation
- **File Upload Security:** Type and size validation

#### Access Control:
- **Permission Decorators:** Endpoint-level security
- **Resource-Level Permissions:** Object-based access
- **Audit Logging:** Security event tracking
- **Session Management:** Secure session handling

---

## 🧪 Testing & Quality Assurance

### 1. Test Coverage

#### Unit Tests:
- **Model Testing:** Data validation and relationships
- **API Testing:** Endpoint functionality
- **Authentication Testing:** Security verification
- **Form Testing:** Validation and submission

#### Integration Tests:
- **Database Integration:** Full-stack testing
- **API Workflow Testing:** End-to-end scenarios
- **Authentication Flow:** Complete auth testing
- **File Upload Testing:** Media handling

### 2. Code Quality

#### Standards Compliance:
- **PEP 8:** Python code standards
- **Type Hints:** Full type annotation
- **Documentation:** Comprehensive docstrings
- **Code Review:** Pull request processes

#### Quality Tools:
- **Black:** Code formatting
- **isort:** Import organization
- **flake8:** Linting and style checking
- **mypy:** Static type checking

---

## 📚 API Usage Examples

### 1. Authentication Flow

#### Complete Registration and Login:
```python
# 1. User Registration
POST /api/users/register
{
  "phone_number": "+1234567890",
  "password": "securepass123",
  "confirm_password": "securepass123",
  "first_name": "John",
  "last_name": "Engineer",
  "email": "john.engineer@railway.com"
}

# Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "Bearer",
  "expires_in": 3600
}

# 2. Subsequent API Calls
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### 2. Wheel Specification Submission

#### Complete Form Submission:
```python
POST /api/forms/wheel-specifications
Authorization: Bearer <token>
{
  "formNumber": "WS-2024-001",
  "submittedBy": "123",
  "submittedDate": "2024-01-15",
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
```

### 3. Bogie Checksheet Inspection

#### Complete Inspection Form:
```python
POST /api/forms/bogie-checksheets
Authorization: Bearer <token>
{
  "formNumber": "BC-2024-001",
  "inspectionBy": "456",
  "inspectionDate": "2024-01-15",
  "bogieDetails": {
    "bogieNo": "B-12345",
    "makerYearBuilt": "ICF/2020",
    "incomingDivAndDate": "Mumbai Division/2024-01-10",
    "deficitComponents": "None",
    "dateOfIOH": "2023-06-15"
  },
  "bogieChecksheet": {
    "bogieFrameCondition": "Good",
    "bolster": "Good",
    "bolsterSuspensionBracket": "Fair",
    "lowerSpringSeat": "Good",
    "axleGuide": "Good"
  },
  "bmbcChecksheet": {
    "cylinderBody": "GOOD",
    "pistonTrunnion": "GOOD",
    "adjustingTube": "FAIR",
    "plungerSpring": "GOOD"
  }
}
```

---

## 🚀 Deployment Guide

### 1. Development Setup

```bash
# Clone repository
git clone <repository-url>
cd KPA_ERP_FE

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Environment configuration
cp .env.example .env
# Edit .env with your settings

# Database setup
createdb kpa_erp_dev
python manage.py migrate
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### 2. Docker Development

```bash
# Start all services
docker-compose up --build

# Database initialization
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# Access application
# API: http://localhost:8000/api/
# Docs: http://localhost:8000/api/docs/
```

### 3. Production Deployment

```bash
# Environment setup
export DJANGO_SETTINGS_MODULE=config.settings.prod
export DB_PASSWORD=<secure_password>
export SECRET_KEY=<secure_secret_key>

# SSL certificates
mkdir ssl
# Copy SSL certificates to ssl/ directory

# Deploy with production compose
docker-compose -f docker-compose.prod.yml up -d

# Static files and migrations
docker-compose exec web python manage.py collectstatic --noinput
docker-compose exec web python manage.py migrate
```

---

## 📋 Configuration Reference

### 1. Environment Variables

```bash
# Django Core
SECRET_KEY=your-secret-key
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.prod

# Database
DB_NAME=kpa_erp
DB_USER=postgres
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432

# JWT Configuration
JWT_SECRET_KEY=jwt-secret-key

# Email Configuration (Production)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=app-password

# Redis (Optional)
REDIS_URL=redis://localhost:6379/1

# File Storage
MEDIA_ROOT=/app/media
STATIC_ROOT=/app/staticfiles
```

### 2. Django Settings

```python
# API Configuration
API_TITLE = "KPA ERP API"
API_VERSION = "1.0.0"
NINJA_PAGINATION_PER_PAGE = 20

# JWT Settings
NINJA_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# CORS Settings
CORS_ALLOW_ALL_ORIGINS = True  # Development only
CORS_ALLOW_CREDENTIALS = True
```

---

## 🔍 Monitoring & Maintenance

### 1. Health Monitoring

#### Health Check Endpoints:
```
GET /health/          # Basic health check
GET /api-info/        # API information
GET /api/             # API root with status
```

#### Monitoring Metrics:
- **Response Times:** API endpoint performance
- **Error Rates:** Failed request tracking
- **Database Performance:** Query execution times
- **Authentication Metrics:** Login success/failure rates

### 2. Logging Configuration

#### Log Levels:
- **DEBUG:** Development troubleshooting
- **INFO:** General operation information
- **WARNING:** Non-critical issues
- **ERROR:** Application errors
- **CRITICAL:** System-level failures

#### Log Categories:
```python
# Application logs
'django.request'     # HTTP request/response
'django.db.backends' # Database queries
'django.security'    # Security events
'apps.users'         # User management
'apps.forms'         # Form operations
```

### 3. Backup Strategy

#### Database Backups:
```bash
# Automated daily backups
pg_dump -h localhost -U postgres kpa_erp > backup_$(date +%Y%m%d).sql

# Restore from backup
psql -h localhost -U postgres -d kpa_erp < backup_20240115.sql
```

#### Media File Backups:
- **File System Backups:** Regular media directory snapshots
- **Cloud Storage Integration:** AWS S3, Google Cloud Storage
- **Version Control:** Track file changes and updates

---

## 🎯 Future Enhancements

### 1. Planned Features

#### Phase 2 Developments:
- **Real-time Notifications:** WebSocket integration for live updates
- **Advanced Reporting:** Dashboard with analytics and insights
- **Mobile Application:** Native mobile app for field workers
- **Barcode Integration:** QR/barcode scanning for equipment tracking
- **Workflow Automation:** Automated approval and routing systems

#### Technical Improvements:
- **Elasticsearch Integration:** Advanced search capabilities
- **GraphQL API:** Alternative query interface
- **Microservices Architecture:** Service decomposition for scaling
- **Event Sourcing:** Audit trail and data history tracking

### 2. Integration Opportunities

#### Enterprise Systems:
- **SAP Integration:** ERP system connectivity
- **HRMS Integration:** Employee data synchronization
- **Asset Management:** Equipment lifecycle tracking
- **Maintenance Scheduling:** Predictive maintenance workflows

#### External APIs:
- **SMS Integration:** Phone-based notifications
- **Email Services:** Advanced email templates
- **Document Generation:** PDF report generation
- **Cloud Storage:** Distributed file storage

---

## 🤝 Support & Maintenance

### 1. Technical Support

#### Documentation Resources:
- **API Documentation:** `/api/docs/` (Swagger UI)
- **OpenAPI Schema:** `/api/openapi.json`
- **Admin Interface:** `/admin/` (Django Admin)
- **Source Code Documentation:** Inline docstrings

#### Common Issues:
- **Authentication Errors:** Token expiration and renewal
- **Validation Failures:** Form data validation troubleshooting
- **Database Connectivity:** Connection and performance issues
- **File Upload Problems:** Media storage and permissions

### 2. Maintenance Procedures

#### Regular Maintenance:
- **Database Optimization:** Index maintenance and query tuning
- **Log Rotation:** Automated log cleanup and archival
- **Security Updates:** Dependency and framework updates
- **Performance Monitoring:** Resource usage and optimization

#### Version Updates:
- **Dependency Management:** Python package updates
- **Database Migrations:** Schema evolution and data migration
- **Feature Deployment:** Rolling updates and rollback procedures
- **Configuration Management:** Environment-specific settings

---

**© 2024 KPA ERP System. All rights reserved.**

*This documentation covers the complete feature set of the KPA ERP System v1.0.0. For technical support, implementation guidance, or feature requests, please contact the development team.* 