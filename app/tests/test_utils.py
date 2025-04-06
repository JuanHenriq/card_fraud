"""Import data from utils"""
from app.utils import processar_dados

def test_processar_dados():
    """Function to insert data"""
    dados = {
        'distance_from_home': '10.5',
        'distance_from_last_transaction': '2',
        'ratio_to_median_purchase_price': '1.2',
        'repeat_retailer': '1',
        'used_chip': '0',
        'used_pin_number': '1',
        'online_order': '0'
    }
    resultado = processar_dados(dados)
    assert resultado == [10.5, 2.0, 1.2, 1, 0, 1, 0]
