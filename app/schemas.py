from pydantic import BaseModel
from typing import Optional


class Invoice(BaseModel):
    invoice_number: Optional[str]
    issue_date: Optional[str]
    seller_name: Optional[str]
    seller_tax_id: Optional[str]
    buyer_name: Optional[str]
    buyer_tax_id: Optional[str]
    net_amount: Optional[float]
    tax_amount: Optional[float]
    gross_amount: Optional[float]
    currency: str = "PLN"