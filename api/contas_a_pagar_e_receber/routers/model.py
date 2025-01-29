from fastapi import APIRouter
from pydantic import BaseModel
from decimal import Decimal

router = APIRouter(prefix="/contas-a-pagar-e-receber")

class ContaPagarReceberResponse(BaseModel): # DTO de response
    id: int
    description: str
    value: Decimal
    type: str # PAGAR, RECEBER
    
class ContaPagarReceberRequest(BaseModel): # DTO de request
    description: str
    value: Decimal
    type: str # PAGAR, RECEBER