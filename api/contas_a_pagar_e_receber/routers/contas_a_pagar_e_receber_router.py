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

@router.get("/")
def listar_contas():
    contas = [
        ContaPagarReceberResponse(
          id=1,
          description="Aluguel",
          value=Decimal("1000.50"),
          type="PAGAR"  
        ),
        ContaPagarReceberResponse(
          id=2,
          description="Salário",
          value=Decimal("5000"),
          type="RECEBER"  
        ),
    ]
    
    return [conta.model_dump() for conta in contas] 
    
@router.post("/", response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(conta: ContaPagarReceberRequest):
    return ContaPagarReceberResponse(
        id=3,
        description=conta.description,
        value=conta.value,
        type=conta.type
    )