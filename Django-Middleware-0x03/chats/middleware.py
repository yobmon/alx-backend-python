import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('requests.log')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class RequestLoggingMiddleware:
    """
    Middleware that logs each user's request with timestamp, user, and path.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Determine the user
        user = request.user if request.user.is_authenticated else 'Anonymous'

        # Log the request
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        # Continue processing the request
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict how many chat messages a user can send
    within a specific time window, based on their IP address.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_requests = {}        # {"ip": [timestamps]}
        self.MAX_MESSAGES = 5        # Limit: 5 messages
        self.WINDOW_SECONDS = 60     # Time window: 1 minute

    def __call__(self, request):
        # Only limit POST requests to message endpoints
        if request.method == "POST" and "/messages" in request.path:
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Initialize IP tracking list
            if ip not in self.ip_requests:
                self.ip_requests[ip] = []

            # Remove requests older than 1 minute
            self.ip_requests[ip] = [
                t for t in self.ip_requests[ip]
                if now - t < timedelta(seconds=self.WINDOW_SECONDS)
            ]

            # Check if rate limit exceeded
            if len(self.ip_requests[ip]) >= self.MAX_MESSAGES:
                return JsonResponse(
                    {"error": "Rate limit exceeded: Only 5 messages allowed per minute."},
                    status=429
                )

            # Add new timestamp
            self.ip_requests[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Retrieves client IP address (handles proxies)."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")

class RolePermissionMiddleware:
    """
    Middleware that restricts access to certain endpoints based on user roles.
    Expected: Users must have a role attribute on the User model.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        # Only check permissions for protected paths
        protected_paths = [
            "/admin-actions",
            "/manage-users",
            "/conversations/admin/",
        ]

        if any(request.path.startswith(p) for p in protected_paths):
            if not user.is_authenticated:
                return JsonResponse(
                    {"error": "Authentication required"},
                    status=401
                )

            # Ensure user has a role attribute, default to 'user'
            user_role = getattr(user, "role", "user")

            if user_role != "admin":
                return JsonResponse(
                    {"error": "You do not have permission to access this resource"},
                    status=403
                )

        return self.get_response(request)