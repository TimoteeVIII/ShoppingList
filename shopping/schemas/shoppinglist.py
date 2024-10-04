from ninja import Field, Schema
from pydantic import UUID4


class ShoppingListCreateSchema(Schema):
    list_name: str = Field(..., min_length=2, max_length=50, alias="list_name")
    household: UUID4 = Field(...)
