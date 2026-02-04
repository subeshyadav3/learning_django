# middlewares to logging requests and responses


from django.utils.deprecation import MiddlewareMixin
from .models import User

class UserActivityLogging(MiddlewareMixin):
    def process_request(self,request):
        user=request.user
        if user.is_authenticated:

            print("User Activity: ", user.username, " accessed ", request.path)
    
    def process_response(self,request,response):
        user=request.user
        if user.is_authenticated:
   

            print("User Activity: ", user.username, " received response with status ", response.status_code)
        return response
    
    
# class IpBlockerMiddleware(MiddlewareMixin):
    