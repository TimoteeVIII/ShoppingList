from django.db import models
from django.contrib.auth.models import User
import uuid


class Household(models.Model):
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, blank=False)
    house_admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    household_name = models.CharField(max_length=50, null=False, default="")


class UserHousehold(models.Model):
    household = models.ForeignKey(Household, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ShoppingList(models.Model):
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    household = models.ForeignKey(Household, on_delete=models.CASCADE)
    list_name = models.CharField(max_length=50, null=False, default="")


class Item(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, blank=False)
    item_name = models.CharField(max_length=50, null=False, default="")
    quantity = models.FloatField()
    completed = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
