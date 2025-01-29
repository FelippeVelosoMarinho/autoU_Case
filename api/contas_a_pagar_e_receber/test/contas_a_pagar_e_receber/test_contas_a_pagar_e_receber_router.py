from fastapi.testclient import TestClient

from main import app

client = TestClient(app) # cliente de testes

def test_deve_listar_contas_a_pagar_e_receber():
    response = client.get('/contas-a-pagar-e-receber')
    
    assert response.status_code == 200
    assert response.json() == [
        {'id': 1, 'description': 'Aluguel', 'value': 1000.5, 'type': 'PAGAR'},
        {'id': 2, 'description': 'Salário', 'value': 5000, 'type': 'RECEBER'}
    ]
    
def test_deve_criar_conta_a_pagar_e_receber():
    nova_conta = {
        "description": "Curso de Python",
        "value": 333,
        "type": "PAGAR"
    }
    
    response = client.post("/contas-a-pagar-e-receber", json=nova_conta)
    assert response.status_code == 201