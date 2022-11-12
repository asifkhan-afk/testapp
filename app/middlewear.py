from urllib import response


class CreatDonerMW:
    def __init__(self,get_response):
        self.get_response=get_response
        print("this is before view middele ware")
    def __call__(self,request):
        print("this is after view")
        response=self.get_response(request)
        print("this is fter mv view")
        return response
        
        
    