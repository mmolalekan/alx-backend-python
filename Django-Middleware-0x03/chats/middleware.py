from datetime import datetime
from django.utils import timezone
from django.http import HttpResponse

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        """
        Logs each user’s requests to a file, including the timestamp, user and the request path
        """
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        
        with open('requests.log', 'a') as log_file:
            log_file.write(log_entry)
        
        response = self.get_response(request)
        
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        """
        Restricts access to the messaging up during certain hours of the day
        """
        server_time = datetime.now().time()
        if server_time.hour < 9 or server_time.hour > 18:
            return HttpResponse("Access to the messaging app is restricted to business hours (9 AM to 6 PM).", status=403)
        
        
        response = self.get_response(request)
        
        return response

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.limit = 5  # max requests
        self.duration = 60  # in seconds
    
    def __call__(self, request):
        """
        Limits the number of chat messages a user can send within a certain time window, based on their IP address.
        """
        ip = self.get_client_ip(request)
        one_minute_ago = timezone.now() - timezone.timedelta(seconds=self.duration)
        request_count = request.session.get(ip, [])
        request_count = [timestamp for timestamp in request_count if timestamp > one_minute_ago]
        if len(request_count) >= self.limit:
            return HttpResponse("Too many requests. Please try again later.", status=429)        
        
        response = self.get_response(request)
        
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        """
        Ensures that only users with specific roles (e.g., admin, moderator) can access certain views or perform specific actions within the messaging app.
        """
        if not request.user.is_authenticated:
            return HttpResponse("You must be logged in to access this resource.", status=401)

        user_role = getattr(request.user, 'role', None)
        
        if not user_role in ['admin', 'moderator']:
            return HttpResponse("You do not have permission to access this resource.", status=403)
        
        response = self.get_response(request)
        
        return response
