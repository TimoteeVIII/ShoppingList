from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from pydantic.types import UUID4

from ninja import Router
from ninja.security import django_auth

from .models import Household, Item, ShoppingList, UserHousehold
from .schemas import household, item, shoppinglist

router = Router()


@router.get("health")
def hello():
    return JsonResponse({"message": "Healthy Shopping App"}, status=200)


@router.get("/userhouses", auth=django_auth)
def get_user_households(request):
    user_households = UserHousehold.objects.filter(user=request.user).select_related("household")
    to_return = {str(uh.household.uuid): uh.household.household_name for uh in user_households}
    if not to_return:
        return JsonResponse({"message": "no houses found"}, status=404)
    return JsonResponse({"data": to_return}, status=200)


@router.post("/household", auth=django_auth)
def create_household(request, payload: household.HouseholdCreateSchema):
    with transaction.atomic():
        new_household = Household.objects.create(
            household_name=payload.household_name,
            house_admin=request.user
        )
        UserHousehold.objects.create(
            household=new_household,
            user=request.user
        )
    return JsonResponse({"message": "Successful"}, status=201)


@router.get("/household/{household_uuid}", auth=django_auth)
def get_shopping_lists(request, household_uuid: UUID4):
    house = get_object_or_404(Household, uuid=household_uuid)
    if not UserHousehold.objects.filter(user=request.user, household=house).exists():
        return JsonResponse({"message": "Invalid"}, status=403)
    house: Household = Household.objects.filter(uuid=household_uuid).first()
    shopping_lists: list[ShoppingList] = ShoppingList.objects.filter(household=house)
    to_return = {str(shopping_list.uuid): shopping_list.list_name for shopping_list in shopping_lists}
    return JsonResponse({"data": to_return}, status=200)


@router.post("/list", auth=django_auth)
def create_list(request, payload: shoppinglist.ShoppingListCreateSchema):
    house = get_object_or_404(Household, uuid=payload.household)
    if not UserHousehold.objects.filter(user=request.user, household=house).exists():
        return JsonResponse({"message": "Invalid"}, status=403)
    with transaction.atomic():
        ShoppingList.objects.create(
            created_by=request.user,
            household=house,
            list_name=payload.list_name,
        )
    return JsonResponse({"message": "Successful"}, status=201)


@router.post("/item", auth=django_auth)
def create_item(request, payload: item.ItemCreateSchema):
    shopping_list: ShoppingList = get_object_or_404(
        ShoppingList.objects.select_related("household"),
        uuid=payload.list_id
    )
    house: Household = shopping_list.household
    if not UserHousehold.objects.filter(user=request.user, household=house).exists():
        return JsonResponse({"message": "Invalid"}, status=403)
    with transaction.atomic():
        Item.objects.create(
            shopping_list=shopping_list,
            item_name=payload.item_name,
            quantity=payload.quantity,
            created_by=request.user,
        )
    return JsonResponse({"message": "Successful"}, status=201)


@router.patch("/item/{item_uuid}", auth=django_auth)
def toggle_completion(request, item_uuid: UUID4):
    list_item: Item = get_object_or_404(
        Item.objects.select_related('shopping_list__household'),
        uuid=item_uuid
    )
    shopping_list: ShoppingList = list_item.shopping_list
    house: Household = shopping_list.household
    if not UserHousehold.objects.filter(user=request.user, household=house).exists():
        return JsonResponse({"message": "Invalid"}, status=403)
    list_item.completed = not list_item.completed
    list_item.save()
    return JsonResponse({"message": "Succesful"}, status=204)


@router.get("/list/{list_id}", auth=django_auth)
def get_list_items(request, list_id: UUID4):
    shopping_list: ShoppingList = get_object_or_404(
        ShoppingList.objects.select_related("household"),
        uuid=list_id
    )
    house: Household = shopping_list.household
    if not UserHousehold.objects.filter(user=request.user, household=house).exists():
        return JsonResponse({"message": "Invalid"}, status=403)
    list_items: list[Item] = Item.objects.filter(shopping_list=shopping_list)
    to_return = {str(list_item.uuid): {
        "name": list_item.item_name,
        "quantity": list_item.quantity,
        "completed": list_item.completed,
    }
        for list_item in list_items
    }
    return JsonResponse({"data": to_return}, status=200)
