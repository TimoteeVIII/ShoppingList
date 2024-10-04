from ninja import Router
from .schemas.user import UserCreateSchema, UserLoginSchema
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from ninja.security import django_auth
from django.http import JsonResponse

router = Router()


@router.get("health")
def hello(request):
    return JsonResponse({"message": "Healthy Application"}, status=200)


@router.get("loggedin", auth=django_auth)
def check_logged_in(request):
    # request.session.cycle_key()
    return JsonResponse({"message": "Logged In"}, status=200)


@router.post("register", response={201: dict, 422: dict, 500: dict})
def register(request, payload: UserCreateSchema):
    try:
        if User.objects.filter(username=payload.username).exists():
            return JsonResponse({"message": "Username taken"}, status=422)

        if User.objects.filter(email=payload.email).exists():
            return JsonResponse({"message": "Email taken"}, status=422)

        with transaction.atomic():
            user = User.objects.create(
                username=payload.username,
                email=payload.email,
                first_name=payload.first_name,
                last_name=payload.last_name,
            )
            user.set_password(payload.password)
            user.save()

        django_login(request, user)
        return JsonResponse({"message": "User created successfully"}, status=201)
    except Exception as e:
        return JsonResponse({"message": "Server Error", "error": str(e)[0]}, status=500)


@router.post("login", response={200: dict, 422: dict, 403: dict})
def login(request, payload: UserLoginSchema):
    if not (payload.username or payload.email):
        return JsonResponse({"message": "Not provided email or username"}, status=422)

    try:
        user = User.objects.get(Q(username=payload.username) | Q(email=payload.email))
        user = authenticate(request, username=user.username, password=payload.password)
    except User.DoesNotExist:
        return JsonResponse({"message": "User doesn't exist"}, status=403)

    if user:
        django_login(request, user)
        return JsonResponse({"message": "Successfully logged in"}, status=200)
    else:
        return JsonResponse({"message": "Invalid credentials"}, status=403)


@router.post("logout", auth=django_auth, response={200: dict})
def logout(request):
    django_logout(request)
    return JsonResponse({"message": "Successfully Logged Out"}, status=200)
