# KPA ERP API

A modern ERP system built with Django and Django Ninja, featuring phone-based JWT authentication and PostgreSQL database.

## Features

- 🔐 **Phone-based Authentication**: JWT authentication using phone numbers instead of email
- 📝 **Dynamic Forms System**: Create and manage dynamic forms with various field types
- 🚂 **Railway Maintenance Forms**: Specialized wheel specifications and bogie checksheet systems
- 👥 **User Management**: Complete user management with roles and permissions
- 🚀 **Django Ninja API**: Fast, modern API framework with automatic OpenAPI documentation
- 🐘 **PostgreSQL**: Robust PostgreSQL database integration with optimized indexing
- 🔧 **Well-structured**: Clean architecture with separate apps for different functionalities
- 🐳 **Docker Ready**: Complete Docker setup for development and production
- 📊 **Swagger Documentation**: Auto-generated API documentation with interactive testing
- 🔒 **Enterprise Security**: JWT token rotation, CORS management, and comprehensive validation
- 📈 **High Performance**: 3-5x faster than Django REST Framework with async support

## 📚 Documentation

- **[📋 Features Summary](./FEATURES_SUMMARY.md)** - Quick overview of all system capabilities
- **[📖 Complete Technical Documentation](./FEATURES_DOCUMENTATION.md)** - Comprehensive technical guide (1000+ lines)
- **[🔗 Interactive API Docs](http://localhost:8000/api/docs/)** - Live API documentation (when running)

## Project Structure

`
KPA_ERP_FE/
├── apps/
│   ├── forms/                  # Core app for form-related APIs
│   │   ├── models/
│   │   ├── serializers/
│   │   ├── views/
│   │   └── admin.py
│   ├── users/                  # Auth, roles, permissions
│   │   ├── models/
│   │   ├── serializers/
│   │   ├── views/
│   │   └── admin.py
│   └── common/                 # Shared utils, constants
│       └── utils/
├── config/                     # Django settings split by env
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── media/                      # File uploads
├── static/                     # Static files
├── .env.example               # Environment variables template
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose setup
├── requirements.txt           # Python dependencies
└── manage.py                  # Django management script
```

## Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL 13+
- Redis (optional, for caching)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd KPA_ERP_FE
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and other settings
   ```

5. **Set up database**
   ```bash
   # Create PostgreSQL database
   createdb kpa_erp


   # make Migration
   python manage.py makemigrations
   
   # Run migrations
   python manage.py migrate
   
   # Create superuser
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - API: http://localhost:8000/api/
   - Documentation: http://localhost:8000/api/docs/
   - Admin: http://localhost:8000/admin/

## Docker Setup

### Development with Docker

```bash
# Build and run with docker-compose
docker-compose up --build

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

### Production Deployment

1. Update environment variables in `.env`
2. Set `DJANGO_SETTINGS_MODULE=config.settings.prod`
3. Deploy with docker-compose

```bash
docker-compose -f docker-compose.yml up -d
```

## API Documentation

The API documentation is automatically generated and available at:
- Swagger UI: http://localhost:8000/api/docs/
- OpenAPI Schema: http://localhost:8000/api/openapi.json

### Authentication

The API uses JWT (JSON Web Tokens) for authentication with phone numbers:

```bash
# Register new user
POST /api/users/register
{
    "phone_number": "+1234567890",
    "password": "securepassword",
    "confirm_password": "securepassword",
    "first_name": "John",
    "last_name": "Doe"
}

# Login
POST /api/users/login
{
    "phone_number": "+1234567890",
    "password": "securepassword"
}

# Use the returned access_token in Authorization header
Authorization: Bearer <access_token>
```

## API Endpoints

### Users
- `POST /api/users/register` - Register new user
- `POST /api/users/login` - Login user
- `POST /api/users/refresh` - Refresh access token
- `GET /api/users/profile` - Get current user profile
- `PUT /api/users/profile` - Update current user profile
- `POST /api/users/change-password` - Change password
- `GET /api/users/users` - List all users (admin only)
- `GET /api/users/users/{id}` - Get user details
- `POST /api/users/users` - Create user (admin only)
- `PUT /api/users/users/{id}` - Update user
- `DELETE /api/users/users/{id}` - Delete user (admin only)



## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Django Settings
SECRET_KEY=your-secret-key
DEBUG=True
DJANGO_SETTINGS_MODULE=config.settings.dev

# Database
DB_NAME=kpa_erp_dev
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret

# Email (for production)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-password
```

### Settings Files

- `config/settings/base.py` - Common settings
- `config/settings/dev.py` - Development settings
- `config/settings/prod.py` - Production settings

## Development

### Code Structure

- **Models**: Database models in `apps/{app}/models/`
- **Serializers**: Pydantic schemas in `apps/{app}/serializers/`
- **Views**: API views using Django Ninja in `apps/{app}/views/`
- **Admin**: Django admin configuration in `apps/{app}/admin.py`

### Adding New Features

1. Create models in appropriate app
2. Create serializers for request/response validation
3. Create API views using Django Ninja routers
4. Add admin configuration if needed
5. Write tests
6. Update documentation

### Running Tests

```bash
python manage.py test
```

### Code Quality

```bash
# Format code
black .

# Check imports
isort .

# Linting
flake8 .
```

## Production Considerations

1. **Security**: Update SECRET_KEY and all passwords
2. **Database**: Use managed PostgreSQL service
3. **Static Files**: Configure proper static file serving
4. **Logging**: Set up centralized logging
5. **Monitoring**: Implement health checks and monitoring
6. **Backup**: Set up database backups
7. **SSL**: Configure HTTPS with proper certificates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team

## Changelog

### v1.0.0
- Initial release with enterprise-grade features
- Phone-based JWT authentication system
- Specialized railway maintenance forms (wheel specifications, bogie checksheets)
- Dynamic forms system with 13 field types
- Enterprise user management with role-based access control
- High-performance Django Ninja API (3-5x faster than DRF)
- PostgreSQL database with optimized indexing
- Complete Docker infrastructure with Nginx and Redis
- Professional documentation suite (1000+ lines of technical docs)
- Auto-generated OpenAPI documentation with Swagger UI
- Production-ready security and performance optimizations 