from django.http import HttpResponse
from ninja import NinjaAPI
from django.views.decorators.csrf import ensure_csrf_cookie


api = NinjaAPI(csrf=True)

api.add_router("auth", "authentication.api.router")
api.add_router("shopping", "shopping.api.router")


@api.get("health")
def hello(request):
    return "Healthy Server!"


@api.get("csrf-token")
@ensure_csrf_cookie
def csrf_token(request):
    return HttpResponse()
