from typing import Optional
from ninja import Schema, Field


class HouseholdCreateSchema(Schema):
    household_name: str = Field(..., min_length=2, max_length=50, alias="household_name")
