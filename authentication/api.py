from ninja import Router
from .schemas.user import UserCreateSchema, UserLoginSchema
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from ninja.security import django_auth

router = Router()


@router.get("health")
def hello(request):
    return 200, {"message": "Healthy Application"}


@router.get("loggedin", auth=django_auth)
def check_logged_in(request):
    return 200, {"message": "Logged In"}


@router.post("register", response={201: dict, 422: dict, 500: dict})
def register(request, payload: UserCreateSchema):
    try:
        if User.objects.filter(username=payload.username).exists():
            return 422, {"message": "Username taken"}

        if User.objects.filter(email=payload.email).exists():
            return 422, {"message": "Email taken"}

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
        return 201, {"message": "User created successfully"}
    except Exception as e:
        return 500, {"message": "Server Error"}


@router.post("login", response={200: dict, 422: dict, 403: dict})
def login(request, payload: UserLoginSchema):
    if not (payload.username or payload.email):
        return 422, {"message": "Not provided email or username"}

    try:
        user = User.objects.get(Q(username=payload.username) | Q(email=payload.email))
        user = authenticate(request, username=user.username, password=payload.password)
    except User.DoesNotExist:
        return 403, {"message": "User doesn't exist"}

    if user:
        django_login(request, user)
        return 200, {"message": "Successfully logged in"}
    else:
        return 403, {"message": "Invalid credentials"}


@router.post("logout", auth=django_auth, response={200: dict})
def logout(request):
    django_logout(request)
    return 200, {"message": "Successfully Logged Out"}
