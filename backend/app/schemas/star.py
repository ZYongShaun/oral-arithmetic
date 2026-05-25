from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class StarBalanceResponse(BaseModel):
    child_id: int
    total_stars: int
    available_stars: int
    spent_stars: int


class StarTransactionResponse(BaseModel):
    id: int
    child_id: int
    amount: int
    balance_after: int
    transaction_type: str
    description: str
    reference_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class StarSpendRequest(BaseModel):
    child_id: int
    amount: int
    transaction_type: str
    description: str


class StarSpendResponse(BaseModel):
    success: bool
    message: str
    balance_before: int
    balance_after: int


class StarShopItem(BaseModel):
    item_id: str
    name: str
    description: str
    cost: int
    icon: str
    available: bool
