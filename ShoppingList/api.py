from ninja import NinjaAPI

api = NinjaAPI()

api.add_router("/auth/", "authentication.api.router")


@api.get("/health")
def hello(request):
    return "Healthy Server!"
