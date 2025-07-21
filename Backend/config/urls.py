"""
URL configuration for KPA ERP project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ninja import NinjaAPI
from ninja.security import HttpBearer
from ninja_jwt.authentication import JWTAuth

from apps.users.views import router as users_router
from apps.forms.api import router as forms_router

# Health check endpoint
@csrf_exempt
def health_check(request):
    """Simple health check endpoint for monitoring"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'KPA ERP API',
        'version': settings.API_VERSION,
        'debug': settings.DEBUG,
        'endpoints': {
            'docs': '/api/docs/',
            'openapi': '/api/openapi.json',
            'users': '/api/users/',
            'admin': '/admin/',
            'health': '/health/'
        }
    })

# API Info endpoint
@csrf_exempt  
def api_info(request):
    """Comprehensive API information endpoint"""
    return JsonResponse({
        'title': settings.API_TITLE,
        'version': settings.API_VERSION,
        'description': 'Car and Wheel Maintenance ERP System API',
        'authentication': {
            'type': 'JWT Bearer Token',
            'header': 'Authorization: Bearer <token>',
            'endpoints': {
                'register': '/api/users/register',
                'login': '/api/users/login',
                'refresh': '/api/users/refresh',
            }
        },
        'main_endpoints': {
            'users': {
                'base_url': '/api/users/',
                'description': 'User management and authentication',
                'methods': ['GET', 'POST', 'PUT', 'DELETE']
            }
        },
        'documentation': {
            'swagger_ui': '/api/docs/',
            'openapi_schema': '/api/openapi.json',
            'redoc': '/api/redoc/'
        },
        'features': [
            'JWT Authentication',
            'User Role Management',
            'PostgreSQL Database',
            'Comprehensive API Documentation'
        ]
    })

# Create the main API instance with enhanced OpenAPI configuration
api = NinjaAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    docs_url="/docs/",
    openapi_url="/openapi.json",
    csrf=False,  # Disable CSRF for API endpoints
    openapi_extra={
        "info": {
            "termsOfService": "https://example.com/terms/",
            "contact": {
                "name": "KPA ERP Support",
                "email": "support@kpa-erp.com",
            },
            "license": {
                "name": "MIT License",
                "url": "https://opensource.org/licenses/MIT",
            },
        },
        "servers": [
            {
                "url": "http://localhost:8000/api",
                "description": "Development server"
            },
            {
                "url": "https://api.kpa-erp.com",
                "description": "Production server"
            }
        ],
        "components": {
            "securitySchemes": {
                "Bearer": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": "JWT token obtained from /users/login endpoint"
                }
            }
        },
        "security": [
            {"Bearer": []}
        ],
        "tags": [
            {
                "name": "Authentication",
                "description": "User registration, login, and token management"
            }
        ]
    }
)

# Add API root endpoint with comprehensive information
@api.get("/", auth=None, tags=["API Info"], include_in_schema=True)
def api_root(request):
    """
    API Root endpoint providing comprehensive information about available endpoints and features.
    
    This endpoint provides a complete overview of the KPA ERP API including:
    - Available endpoints and their purposes
    - Authentication requirements and methods
    - Feature overview
    - Documentation links
    """
    return {
        "message": "Welcome to KPA ERP API",
        "version": settings.API_VERSION,
        "documentation": "Visit /api/docs/ for interactive API documentation",
        "authentication": {
            "required": "JWT Bearer token for most endpoints",
            "register": "/api/users/register",
            "login": "/api/users/login"
        },
        "endpoints": {
            "users": "/api/users/ - User management and authentication",
            "docs": "/api/docs/ - Interactive API documentation",
            "openapi": "/api/openapi.json - OpenAPI specification"
        }
    }

# Add health check endpoint to API
@api.get("/health", auth=None, tags=["Monitoring"], include_in_schema=True)
def api_health(request):
    """
    API Health check endpoint for monitoring and status verification.
    
    Returns the current status of the API service along with basic system information.
    Useful for load balancers, monitoring systems, and health checks.
    """
    return {
        "status": "healthy",
        "service": "KPA ERP API",
        "version": settings.API_VERSION,
        "debug_mode": settings.DEBUG,
        "database": "PostgreSQL",
        "authentication": "JWT",
        "timestamp": "2024-01-01T00:00:00Z"  # This would be dynamic in real implementation
    }

# Add routers to the main API
api.add_router("/users/", users_router, tags=["Users", "Authentication"])
api.add_router("/forms/", forms_router, tags=["Forms", "Specifications", "Checksheets"])

# URL patterns
urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', api.urls),
    
    # Standalone health check (for load balancers that don't use /api/ prefix)
    path('health/', health_check, name='health-check'),
    
    # API information endpoint
    path('api-info/', api_info, name='api-info'),
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Add debug URLs if django-debug-toolbar is installed
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass 