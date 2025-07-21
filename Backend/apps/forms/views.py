"""
View logic for the forms app.
This file contains view-related functionality for the forms app.
All API functionality has been removed.
"""
from django.http import JsonResponse
from django.views import View


class HealthCheckView(View):
    """
    Simple health check view for monitoring purposes.
    """
    def get(self, request):
        return JsonResponse({
            'status': 'healthy',
            'service': 'forms',
            'version': '1.0.0'
        })


# Export only the basic views
__all__ = ['HealthCheckView'] 