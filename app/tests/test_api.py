import pytest
from app.api import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

# Teste funcional: index
def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert "Verificador de Transação" in response.get_data(as_text=True)

# Teste funcional + técnica de partição de equivalência
def test_predict_valid_input(client):
    dados = {
        'distance_from_home': '5',
        'distance_from_last_transaction': '2',
        'ratio_to_median_purchase_price': '1',
        'repeat_retailer': '1',
        'used_chip': '1',
        'used_pin_number': '1',
        'online_order': '0'
    }
    response = client.post('/predict', data=dados, follow_redirects=True)
    assert response.status_code == 200
    assert "Dashboard de Verificação de Fraudes" in response.get_data(as_text=True)

# Teste com valores limites
def test_predict_valor_limite(client):
    dados = {
        'distance_from_home': '0',
        'distance_from_last_transaction': '0',
        'ratio_to_median_purchase_price': '0',
        'repeat_retailer': '0',
        'used_chip': '0',
        'used_pin_number': '0',
        'online_order': '0'
    }
    response = client.post('/predict', data=dados, follow_redirects=True)
    assert response.status_code == 200

# Teste com valores inválidos (partição inválida)
def test_predict_valores_invalidos(client):
    dados = {
        'distance_from_home': '-1',
        'distance_from_last_transaction': 'abc',
        'ratio_to_median_purchase_price': '',
        'repeat_retailer': '2',
        'used_chip': 'maybe',
        'used_pin_number': 'False',
        'online_order': 'yes'
    }
    response = client.post('/predict', data=dados, follow_redirects=True)
    assert response.status_code in [400, 500] 
