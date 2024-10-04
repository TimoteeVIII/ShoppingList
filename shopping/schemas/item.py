from ninja import Field, Schema
from pydantic.types import UUID4


class ItemCreateSchema(Schema):
    item_name: str = Field(..., min_length=2, max_length=50, alias="item_name")
    quantity: float = Field(..., alias="quantity")
    list_id: UUID4 = Field(..., alias="list_id")
