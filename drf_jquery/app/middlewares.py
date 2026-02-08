from datetime import datetime

class UserActivityLogging:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user.username if request.user.is_authenticated else "Anonymous"

        log = (
            f"[{datetime.now()}] "
            f"User: {user} | "
            f"Method: {request.method} | "
            f"Path: {request.path}\n"
        )

        with open("request_log.txt", "a", encoding="utf-8") as f:
            f.write(log)

        return self.get_response(request)
