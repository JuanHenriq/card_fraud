from app.model_loader import model

def test_model_prediction():
    X = [[5.0, 3.0, 1.0, 0, 1, 1, 0]]
    y_pred = model.predict(X)
    assert y_pred[0] in [0, 1]  # Valor esperado de uma predição binária
    