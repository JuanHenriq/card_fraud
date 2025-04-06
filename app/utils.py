def processar_dados(dados):
    return [
        float(dados['distance_from_home']),
        float(dados['distance_from_last_transaction']),
        float(dados['ratio_to_median_purchase_price']),
        int(dados['repeat_retailer']),
        int(dados['used_chip']),
        int(dados['used_pin_number']),
        int(dados['online_order'])
    ]