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

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Store requests per IP: { "ip": [timestamps] }
        self.ip_requests = {}

        # Limit and time window
        self.MAX_MESSAGES = 5
        self.WINDOW_SECONDS = 60

    def __call__(self, request):
        # Only limit POST requests to messaging endpoints
        if request.method == "POST" and "/messages" in request.path:
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Initialize list if new IP
            if ip not in self.ip_requests:
                self.ip_requests[ip] = []

            # Keep only timestamps within last minute
            self.ip_requests[ip] = [
                t for t in self.ip_requests[ip]
                if now - t < timedelta(seconds=self.WINDOW_SECONDS)
            ]

            # Check if user exceeded limit
            if len(self.ip_requests[ip]) >= self.MAX_MESSAGES:
                return JsonResponse(
                    {
                        "error": "Rate limit exceeded: You can only send 5 messages per minute."
                    },
                    status=429
                )

            # Record new request
            self.ip_requests[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Extracts client IP even behind proxies."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")