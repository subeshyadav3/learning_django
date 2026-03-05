import datetime

class RequestLogMiddleware:

    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):

        print("Request Path:",request.path)
        print("Time:",datetime.datetime.now())

        response = self.get_response(request)

        return response