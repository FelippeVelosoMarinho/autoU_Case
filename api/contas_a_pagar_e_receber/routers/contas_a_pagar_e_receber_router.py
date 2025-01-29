from fastapi import APIRouter
from pydantic import BaseModel
from decimal import Decimal

router = APIRouter(prefix="/contas-a-pagar-e-receber")

class ContaPagarReceberResponse(BaseModel): # DTO de response
    id: int
    description: str
    value: Decimal
    type: str # PAGAR, RECEBER

@router.get("/")
def listar_contas():
    return [
        {"conta1": "conta1"},
        {"conta2": "conta2"},
    ]