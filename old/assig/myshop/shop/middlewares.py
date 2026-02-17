import datetime

class UserActionLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            log_line = f"{datetime.datetime.now()} | {user.username} | {request.method} | {request.path}\n"
            with open('log.txt', 'a') as f:
                f.write(log_line)

        return response
