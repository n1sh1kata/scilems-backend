from functools import wraps
import time
import threading
from rest_framework.response import Response
from rest_framework import status

class RateLimiter:
    def __init__(self):
        self.requests = {}  # Dictionary to store request timestamps
        self.lock = threading.Lock()  # Thread-safe lock

    def add_request(self, key, window):
        current_time = time.time()
        with self.lock:
            # Get list of timestamps for this key
            timestamps = self.requests.get(key, [])
            
            # Remove old timestamps
            timestamps = [t for t in timestamps if current_time - t < window]
            
            # Add new timestamp
            timestamps.append(current_time)
            
            # Update dictionary
            self.requests[key] = timestamps
            
            return len(timestamps)

# Global rate limiter instance
rate_limiter = RateLimiter()

def rate_limit(requests=5, window=60):
    """
    Rate limiting decorator that limits the number of requests within a time window.
    
    Args:
        requests (int): Maximum number of requests allowed within the window
        window (int): Time window in seconds
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(view_instance, request, *args, **kwargs):
            # Create a unique key for each client using their IP
            client_ip = request.META.get('REMOTE_ADDR')
            key = f'rate_limit:{client_ip}:{view_func.__name__}'
            
            # Count requests in the current window
            request_count = rate_limiter.add_request(key, window)
            
            # Check if request limit is exceeded
            if request_count > requests:
                return Response({
                    'error': 'Too many requests',
                    'detail': f'Please wait {window} seconds before trying again.',
                    'retry_after': window
                }, status=status.HTTP_429_TOO_MANY_REQUESTS,
                headers={
                    'Retry-After': str(window)
                })
            
            return view_func(view_instance, request, *args, **kwargs)
        return wrapped_view
    return decorator