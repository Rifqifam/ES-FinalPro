from ninja import NinjaAPI

expert_API = NinjaAPI()

@expert_API.get("/hello")
def hello(request):
    return "Hello world"
