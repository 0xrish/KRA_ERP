# 🚆 KPA ERP System - Full Stack Railway Management Solution

![Database Architecture](./media/ERP_DB.png)

## 📋 Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Backend Architecture](#backend-architecture)
- [Frontend Architecture](#frontend-architecture)
- [Backend-Frontend Integration](#backend-frontend-integration)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [API Documentation](#api-documentation)
- [Authentication System](#authentication-system)
- [Database Schema](#database-schema)
- [Documentation Links](#documentation-links)
- [Deployment](#deployment)
- [Contributing](#contributing)

## 🎯 Overview

KPA ERP is a comprehensive Enterprise Resource Planning system specifically designed for railway maintenance management. The system provides digital form submission capabilities, user management, and real-time data processing for railway operations including wheel specifications and bogie checksheet management.

### System Components

- **Backend**: Django + Django Ninja API (Python)
- **Frontend**: Flutter (Cross-platform mobile/web application)
- **Database**: PostgreSQL with optimized indexing
- **Authentication**: JWT-based phone number authentication
- **API**: RESTful APIs with automatic OpenAPI documentation

## 🏗️ System Architecture

```
┌─────────────────┐    HTTP/HTTPS     ┌──────────────────┐
│   Flutter App   │ ◄─────────────── │   Django API     │
│   (Frontend)    │     JSON/REST     │   (Backend)      │
└─────────────────┘                   └──────────────────┘
         │                                       │
         │                                       │
         ▼                                       ▼
┌─────────────────┐                   ┌──────────────────┐
│  Local Storage  │                   │   PostgreSQL     │
│  (SharedPrefs)  │                   │   Database       │
└─────────────────┘                   └──────────────────┘
```

## 🔧 Backend Architecture

### Django + Django Ninja Framework

The backend is built using Django with Django Ninja API framework, providing:

- **High Performance**: 3-5x faster than Django REST Framework
- **Modern API**: Type-safe APIs with automatic validation
- **Phone-based Auth**: JWT authentication using phone numbers
- **Dynamic Forms**: Flexible form system for various railway inspections
- **Enterprise Security**: Token rotation, CORS management, validation

### Backend Structure

```
Backend/
├── apps/
│   ├── forms/              # Core form management
│   │   ├── models/         # Database models
│   │   ├── serializers/    # Pydantic schemas
│   │   ├── views/          # API endpoints
│   │   └── admin.py        # Admin interface
│   ├── users/              # Authentication & user management
│   │   ├── models/         # User models
│   │   ├── serializers/    # User schemas
│   │   ├── views/          # Auth endpoints
│   │   └── admin.py
│   └── common/             # Shared utilities
│       └── utils/
├── config/                 # Django configuration
│   ├── settings/           # Environment-based settings
│   ├── urls.py             # URL routing
│   ├── wsgi.py             # WSGI application
│   └── asgi.py             # ASGI application
├── media/                  # File uploads
├── static/                 # Static files
├── requirements.txt        # Python dependencies
├── manage.py              # Django management
└── docker-compose.yml     # Docker configuration
```

### Key Backend Features

1. **Phone-based Authentication**
   - JWT token system
   - Secure token refresh mechanism
   - Role-based access control

2. **Dynamic Forms System**
   - Wheel Specifications Form
   - Bogie Checksheet Form
   - Extensible form architecture

3. **Enterprise APIs**
   - Auto-generated OpenAPI documentation
   - Type-safe request/response validation
   - Comprehensive error handling

4. **Database Optimization**
   - PostgreSQL with custom indexing
   - Optimized queries
   - Data integrity constraints

## 📱 Frontend Architecture

### Flutter Cross-Platform Application

The frontend is built using Flutter, providing:

- **Cross-Platform**: Single codebase for Android, iOS, and Web
- **Modern UI**: Material Design components
- **State Management**: Provider pattern
- **Offline Capability**: Local storage with sync
- **Real-time Updates**: Live form submissions and status

### Frontend Structure

```
Frontend/
├── lib/
│   ├── models/             # Data models
│   ├── services/           # API service layer
│   │   ├── form_services/  # Form API calls
│   │   ├── authentication_services/  # Auth services
│   │   └── api_services/   # Base API service
│   ├── screens/            # UI screens
│   ├── widgets/            # Reusable components
│   ├── provider/           # State management
│   ├── utils/              # Utility functions
│   ├── constants/          # App constants
│   ├── main.dart           # App entry point
│   └── routes.dart         # Navigation routing
├── assets/                 # Static assets
├── android/                # Android-specific code
├── ios/                    # iOS-specific code
├── web/                    # Web-specific code
└── pubspec.yaml           # Flutter dependencies
```

### Key Frontend Features

1. **Authentication Flow**
   - Phone number login
   - OTP verification
   - JWT token management
   - Automatic token refresh

2. **Form Management**
   - ICF Wheel Specifications
   - ICF Bogie Checksheet
   - Real-time validation
   - Offline form drafting

3. **User Experience**
   - Responsive design
   - Loading states
   - Error handling
   - Success feedback

## 🔗 Backend-Frontend Integration

### API Communication

1. **Authentication Flow**
   ```
   Flutter App                    Django API
        │                            │
        ├── POST /api/users/login ──→│ 
        │← JWT tokens ───────────────┤
        │                            │
        ├── Authorized requests ────→│
        │  (Bearer token)            │
        │← JSON response ────────────┤
   ```

2. **Form Submission Flow**
   ```
   User Input → Validation → API Call → Database → Response → UI Update
   ```

### Data Flow

1. **User Authentication**
   - User enters phone number in Flutter app
   - App sends credentials to Django API
   - Django validates and returns JWT tokens
   - Flutter stores tokens in SharedPreferences
   - Tokens included in all subsequent API calls

2. **Form Operations**
   - User fills form in Flutter UI
   - Form data validated on frontend
   - Data serialized and sent to Django API
   - Django processes and stores in PostgreSQL
   - Success/error response sent back to Flutter
   - UI updated with feedback

### Key Integration Points

- **Service Layer**: Flutter's `FormService` handles all API communications
- **State Management**: Provider pattern manages form state and API responses
- **Error Handling**: Comprehensive error handling on both frontend and backend
- **Data Synchronization**: Real-time sync between mobile app and server
- **Authentication**: Seamless JWT token management across platforms

## ✨ Key Features

### 🔐 Authentication & Security
- Phone-based JWT authentication
- Secure token rotation
- Role-based access control
- CORS protection
- Input validation and sanitization

### 📝 Form Management
- **ICF Wheel Specifications**: Digital wheel inspection forms
- **ICF Bogie Checksheet**: Multi-section bogie inspection forms
- Dynamic form field validation
- Search and filter capabilities
- Form status tracking

### 👥 User Management
- Complete user lifecycle management
- Role and permission system
- User profile management
- Admin dashboard

### 📊 Data Management
- PostgreSQL database with optimized schema
- Real-time data synchronization
- Comprehensive audit trails
- Data export capabilities

### 📱 Mobile Features
- Cross-platform mobile application
- Offline form drafting
- Camera integration for inspections
- GPS location tracking
- Push notifications

## 🛠️ Technology Stack

### Backend Technologies
- **Framework**: Django 5.2.4 + Django Ninja 1.4.3
- **Database**: PostgreSQL with psycopg2
- **Authentication**: JWT with django-ninja-jwt
- **Validation**: Pydantic schemas
- **API Documentation**: Auto-generated OpenAPI/Swagger
- **Deployment**: Docker + Docker Compose

### Frontend Technologies
- **Framework**: Flutter (Dart 3.8.1+)
- **State Management**: Provider 6.1.2
- **HTTP Client**: Built-in Dart HTTP
- **Authentication**: JWT token management
- **Local Storage**: SharedPreferences
- **UI Components**: Material Design

### Development Tools
- **Version Control**: Git
- **Containerization**: Docker
- **API Testing**: Swagger UI + Postman
- **Code Quality**: Black, isort, flake8 (Python) + Flutter linter

## 📁 Project Structure

```
KPA_ERP_FE/
├── Backend/                 # Django API Backend
│   ├── apps/               # Django applications
│   ├── config/             # Django configuration
│   ├── requirements.txt    # Python dependencies
│   ├── manage.py          # Django management
│   └── docker-compose.yml # Docker setup
├── Frontend/               # Flutter Mobile App
│   ├── lib/               # Flutter source code
│   ├── assets/            # Static assets
│   ├── pubspec.yaml       # Flutter dependencies
│   └── README.md          # Frontend docs
├── media/                  # Shared media files
│   └── ERP_DB.png         # Database diagram
└── README.md              # This file
```

## 🚀 Setup Instructions

### Prerequisites

- **Backend**: Python 3.12+, PostgreSQL 13+, Docker (optional)
- **Frontend**: Flutter SDK 3.8.1+, Dart SDK
- **Database**: PostgreSQL server running

### Backend Setup

1. **Clone and Setup Environment**
   ```bash
   git clone <repository-url>
   cd KPA_ERP_FE/Backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Database Configuration**
   ```bash
   # Create PostgreSQL database
   createdb kpa_erp_dev
   
   # Copy environment template
   cp .env.example .env
   # Edit .env with your database credentials
   ```

3. **Run Migrations and Start Server**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

4. **Access Backend**
   - API: http://localhost:8000/api/
   - Documentation: http://localhost:8000/api/docs/
   - Admin: http://localhost:8000/admin/

### Frontend Setup

1. **Setup Flutter Environment**
   ```bash
   cd KPA_ERP_FE/Frontend
   flutter pub get
   ```

2. **Configure API Endpoints**
   ```dart
   // Update API base URL in lib/services/api_services/
   const String baseUrl = 'http://localhost:8000'; // Development
   ```

3. **Run Flutter Application**
   ```bash
   # For development
   flutter run
   
   # For web
   flutter run -d web
   
   # For specific device
   flutter devices
   flutter run -d <device-id>
   ```

### Docker Setup (Alternative)

```bash
# Backend with Docker
cd Backend
docker-compose up --build

# Run migrations in container
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## 📖 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users/register` | Register new user |
| POST | `/api/users/login` | User login |
| POST | `/api/users/refresh` | Refresh token |
| GET | `/api/users/profile` | Get user profile |
| PUT | `/api/users/profile` | Update profile |

### Form Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/forms/wheel-specifications` | Submit wheel form |
| GET | `/api/forms/wheel-specifications` | Get wheel forms |
| POST | `/api/forms/bogie-checksheet` | Submit bogie form |
| GET | `/api/forms/bogie-checksheets` | Get bogie forms |

### Authentication Example

```bash
# Login
curl -X POST http://localhost:8000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+1234567890", "password": "password"}'

# Use token
curl -X GET http://localhost:8000/api/users/profile \
  -H "Authorization: Bearer <access_token>"
```

## 🔐 Authentication System

### JWT Token Flow

1. **User Registration/Login**
   - User provides phone number and password
   - Backend validates credentials
   - Returns access token (15 min) and refresh token (7 days)

2. **Token Usage**
   - Frontend stores tokens in SharedPreferences
   - Access token included in Authorization header
   - Automatic token refresh when expired

3. **Security Features**
   - Phone-based authentication (more secure than email)
   - Token rotation on refresh
   - Secure token storage
   - Automatic logout on token expiration

## 🗄️ Database Schema

The database schema includes the following main entities:

- **Users**: Phone-based user authentication and profiles
- **Forms**: Dynamic form definitions and submissions
- **WheelSpecifications**: Railway wheel inspection data
- **BogieChecksheets**: Bogie inspection checklists
- **Permissions**: Role-based access control

*See the database diagram above for complete schema visualization.*

## 📚 Documentation Links

### Backend Documentation

- **[📋 Backend README](./Backend/README.md)** - Complete backend setup, API endpoints, and development guide
- **[⚡ Features Summary](./Backend/FEATURES_SUMMARY.md)** - Quick overview of all system capabilities and features
- **[📖 Technical Documentation](./Backend/FEATURES_DOCUMENTATION.md)** - Comprehensive technical guide (1000+ lines) with detailed implementation details
- **[🔗 Live API Documentation](http://localhost:8000/api/docs/)** - Interactive Swagger UI documentation (when backend is running)
- **[📊 OpenAPI Schema](http://localhost:8000/api/openapi.json)** - Raw OpenAPI specification (when backend is running)

### Frontend Documentation

- **[📱 Frontend README](./Frontend/README.md)** - Flutter app setup and ICF forms documentation
- **[🔌 API Integration Guide](./Frontend/lib/README_API_Integration.md)** - How frontend integrates with backend APIs

### Quick Access

| Documentation Type | Description | Link |
|-------------------|-------------|------|
| **Getting Started** | Basic setup and installation | [Backend README](./Backend/README.md) |
| **API Reference** | All endpoints and examples | [Live API Docs](http://localhost:8000/api/docs/) |
| **Feature Overview** | What the system can do | [Features Summary](./Backend/FEATURES_SUMMARY.md) |
| **Deep Dive** | Technical implementation details | [Technical Docs](./Backend/FEATURES_DOCUMENTATION.md) |
| **Mobile App** | Flutter frontend guide | [Frontend README](./Frontend/README.md) |
| **Integration** | Backend-Frontend connection | [API Integration](./Frontend/lib/README_API_Integration.md) |

### Development Resources

- **Admin Interface**: http://localhost:8000/admin/ (when running)
- **API Base URL**: http://localhost:8000/api/
- **Database Diagram**: [ERP_DB.png](./media/ERP_DB.png)

## 🚀 Deployment

### Production Backend Deployment

1. **Environment Configuration**
   ```bash
   export DJANGO_SETTINGS_MODULE=config.settings.prod
   export SECRET_KEY=<production-secret>
   export DB_PASSWORD=<secure-password>
   ```

2. **Docker Production**
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

### Frontend Deployment

1. **Build for Production**
   ```bash
   # Android APK
   flutter build apk --release
   
   # iOS
   flutter build ios --release
   
   # Web
   flutter build web --release
   ```

2. **Deploy to Stores**
   - Follow platform-specific deployment guides
   - Configure production API endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow Django and Flutter coding standards
- Write comprehensive tests
- Update documentation
- Ensure API compatibility
- Test across platforms

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the API documentation at `/api/docs/`

---

**Made with ❤️ for Railway Management Systems**

*KPA ERP - Streamlining Railway Operations Through Digital Innovation* 