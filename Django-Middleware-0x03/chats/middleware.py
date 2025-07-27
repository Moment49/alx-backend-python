import os
import logging
from datetime import datetime


# This gets the full file path to where we can log the requests
full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../requests.log'))

# Set up logging
logging.basicConfig(filename=full_path,
                    format='%(asctime)s %(message)s',
                    filemode='a')

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
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

        
        response = self.get_response(request)
        