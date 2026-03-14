import datetime
import os

class RequestLogMiddleware:
    """
    Middleware to log every request to a file,
    including timestamp, user, session ID, path, and cookies.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        os.makedirs(os.path.dirname(__file__), exist_ok=True)   
        self.log_file_path = os.path.join(os.path.dirname(__file__), "logs.txt")

    def __call__(self, request):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user = request.user.username if request.user.is_authenticated else "Anonymous"
        session_id = request.session.session_key or "No Session"
        path = request.path
        method = request.method
        cookies = request.COOKIES

        log_line = (
            f"[{timestamp}] User: {user} | SessionID: {session_id} | "
            f"Method: {method} | Path: {path} | Cookies: {cookies}\n"
        )

        # Append log to file
        with open(self.log_file_path, "a") as f:
            f.write(log_line)

        # Also print to console
        print(log_line.strip())

        response = self.get_response(request)
        return response