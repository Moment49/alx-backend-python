import os
import logging
from datetime import datetime, time
from .models import Message
from rest_framework.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseForbidden


# This gets the full file path to where we can log the requests
full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../requests.log'))

# Set up logging
logging.basicConfig(filename=full_path,
                    format='%(asctime)s %(message)s',
                    filemode='a')

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
    
    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # Get the request path and request user and log it
        print("before hitting the view")
        user = request.user
        print(user)
        # Log the info to the log file about the user
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
                    
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
    

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check the current server time
        server_time = datetime.now()
        start_window = time(hour=18, minute=0, second=0)
        end_window = time(hour=21, minute=0, second=0)

        response = self.get_response(request)

        if request.user.is_authenticated and request.method == "GET" and request.path.endswith('message/'):
            # Check if the current time has been exceeded from 6pm to 9pm
            if Message.objects.filter(sender = request.user).exists():
                if server_time.time() >= start_window and server_time.time() <= end_window:
                   logger.info("You can access the message/chats that belongs to you")
                else:
                    return HttpResponseForbidden("Sorry, access denied you cannot access the message/chats outside the time 6pm - 9pm")
        
        return response

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        chat_sent_ip_addr_count = 0
        max_sent_message_per_min = 5
        self.tracker_ip = {}
    
    def __call__(self, request):
        
        response = self.get_response(request)

        return response