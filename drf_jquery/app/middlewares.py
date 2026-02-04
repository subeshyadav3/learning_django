
from django.utils.deprecation import MiddlewareMixin

from datetime import datetime

class UserActivityLogging(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        log = f"[{datetime.now()}] {request.method} {request.path}\n"

        with open("request_log.txt", "a") as f:
            f.write(log)

        return self.get_response(request)
