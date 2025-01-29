from contas_a_pagar_e_receber.routers.model import ContaPagarReceberResponse, ContaPagarReceberRequest, router, Decimal

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