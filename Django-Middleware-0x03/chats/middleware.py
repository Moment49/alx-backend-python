import os
import logging
from datetime import datetime, time, timedelta
from .models import Message
from rest_framework.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


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
        user = request.user
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
        # One-time configuration and initialization
        self.get_response = get_response
        self.tracker_ip = {}  # Dictionary to track IP addresses, their request counts, and timestamps
    
    def __call__(self, request):
        # Extract the client's IP address from request headers
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip_address:
            ip_address = ip_address.split(',')[0]  # In case of multiple forwarded IPs
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        # Get the current time for request timestamping
        start_time = datetime.now()
        # Check if the user is autheticated
        
        # Call the view (and next middleware after this one)
        response = self.get_response(request)
       
        # Proceed only if the user is authenticated and accessing the message POST endpoint
        if request.user.is_authenticated and request.method == "POST" and request.path == "/api/v1/message/":
            ip_count = 1 # Start with a count of 1 for new IPs

            if ip_address not in self.tracker_ip:
                # First-time request from this IP — initialize tracking
                self.tracker_ip[ip_address] = {
                    "start_time":start_time,
                    "ip_count":ip_count
                }
                logger.info(f"First time: {ip_address}:{self.tracker_ip.get(ip_address)}")
            else:
                # Existing IP — increment the request count
                current_time = datetime.now()
                self.tracker_ip[ip_address]['ip_count'] += 1
                logger.info(f"Ip already exists increment:{self.tracker_ip}")
               
                # Calculate the time difference from the first request
                time_diff = current_time - self.tracker_ip[ip_address]['start_time']

                # If too many requests within 1 minute, block the request
                if time_diff < timedelta(minutes=1) and self.tracker_ip[ip_address].get('ip_count') > 5:
                    logger.warning(f"Sorry you have exceeded the number of request in a minute by Ip {ip_address}")
                    return HttpResponseForbidden("Sorry you have exceeded the number of request in a minute. " \
                    "Wait a minute and try again")
                
                # If more than a minute has passed, reset count and timestamp
                if time_diff > timedelta(minutes=1):
                    self.tracker_ip[ip_address]['ip_count'] = 1
                    self.tracker_ip[ip_address]['start_time'] = current_time

        # Return the response from the view        
        return response


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # This block runs on every request before the view is processed

        # Check if the user is authenticated and a request method exists and path is not root path
        # Even if you are not authenticated you can visit the main url
       
        # Get the Ip address of the user if not from user is connecting from a proxy
        ip_addr = request.META.get("HTTP_X_FORWARDED_FOR")
        if ip_addr:
            ip_addr = ip_addr.split(',')[0]
        else:
            ip_addr = request.META.get("REMOTE_ADDR")
       
        if request.user.is_authenticated and request.method and request.path != '/':
            user = request.user
            try:
                # Retrieve the user from the database using their email
                user = CustomUser.objects.get(email=user.email)
            except CustomUser.DoesNotExist:
                # Deny access if the user does not exist in the database and log there IP for investigation
                logger.info(f"Access denied: Invalid user with IP: {ip_addr}")
                return HttpResponseForbidden("Access denied: Invalid user account.")
            
            # Check if the user has one of the allowed roles
            if not user.role in ['ADMIN', 'HOST', 'MODERATOR', 'GUEST']:
                # Deny access if the user's role is not permitted
                return HttpResponseForbidden(
                    "Sorry you are not an admin, host or moderator"
                    )
            
        # Proceed to the next middleware or view
        response = self.get_response(request)
        return response