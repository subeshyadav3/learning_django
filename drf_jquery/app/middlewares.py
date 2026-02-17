from datetime import datetime
import logging
import os
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

# Setup logging
logger = logging.getLogger(__name__)


class UserActivityLoggingMiddleware(MiddlewareMixin):
    """
    Middleware for comprehensive user activity logging.
    Logs all requests with timestamp, user, method, path, and response status.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.log_file = "request_log.txt"

    def __call__(self, request):
        # Log request details
        self.log_request(request)
        response = self.get_response(request)
        # Log response details
        self.log_response(request, response)
        return response

    def log_request(self, request):
        """Log incoming request details"""
        user = request.user.username if request.user.is_authenticated else "Anonymous"
        
        log_message = (
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"REQUEST | User: {user} | "
            f"Method: {request.method} | "
            f"Path: {request.path} | "
            f"IP: {self.get_client_ip(request)}\n"
        )
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_message)
        
        logger.info(log_message.strip())

    def log_response(self, request, response):
        """Log outgoing response details"""
        user = request.user.username if request.user.is_authenticated else "Anonymous"
        
        log_message = (
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"RESPONSE | User: {user} | "
            f"Status: {response.status_code} | "
            f"Path: {request.path}\n"
        )
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_message)
        
        logger.info(log_message.strip())

    @staticmethod
    def get_client_ip(request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Middleware for adding security headers to responses.
    Helps prevent common security vulnerabilities.
    """

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
        
        return response


class ErrorHandlingMiddleware(MiddlewareMixin):
    """
    Middleware for comprehensive error handling.
    Catches exceptions and logs them appropriately.
    """

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            logger.error(f"Error handling request {request.path}: {str(e)}", exc_info=True)
            
            error_log = (
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                f"ERROR | Path: {request.path} | "
                f"Error: {str(e)}\n"
            )
            
            with open("error_log.txt", "a", encoding="utf-8") as f:
                f.write(error_log)
            
            # Return JSON error response for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': 'An error occurred processing your request.'
                }, status=500)
            
            # For regular requests, raise the exception (Django will handle it)
            raise

        return response


class SessionHandlingMiddleware(MiddlewareMixin):
    """
    Middleware for enhanced session handling.
    Manages session data and handles session expiration.
    """

    def __call__(self, request):
        # Initialize session data if not present
        if request.user.is_authenticated:
            if 'user_login_time' not in request.session:
                request.session['user_login_time'] = datetime.now().isoformat()
            
            if 'cart' not in request.session:
                request.session['cart'] = {}
        
        response = self.get_response(request)
        return response


class CustomHeadersMiddleware(MiddlewareMixin):
    """
    Middleware for adding custom headers to track request/response flow.
    Useful for debugging and monitoring.
    """

    def __call__(self, request):
        request.request_id = datetime.now().timestamp()
        response = self.get_response(request)
        
        response['X-Request-ID'] = str(request.request_id)
        response['X-Processed-By'] = 'CustomHeadersMiddleware'
        
        return response

