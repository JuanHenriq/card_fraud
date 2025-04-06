from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
import sqlite3
import pandas as pd
from .model_loader import model
from .database import init_db
from .utils import processar_dados
import os

app = Flask(
    __name__,
    static_url_path='/static',
    static_folder=os.path.join(os.path.dirname(__file__), 'static'),
    template_folder=os.path.join(os.path.dirname(__file__), 'templates')
)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect('app/predicoes.db')
    df = pd.read_sql_query("SELECT * FROM predicoes", conn)
    conn.close()

    if not df.empty:
        total = len(df)

        # Percentual de predições por classe
        fraud_counts = df['predicao'].value_counts().sort_index().tolist()

        # Dados para gráfico de dispersão
        distances = df['distance_from_home'].tolist()
        labels = df['predicao'].tolist()

        # Estatísticas descritivas
        stats = df.describe().round(2).to_html(classes="table")

        # Contagens para gráficos de pizza dos campos booleanos
        campos_booleanos = ['repeat_retailer', 'used_chip', 'used_pin_number', 'online_order']
        pizzas = {campo: df[campo].value_counts().sort_index().tolist() for campo in campos_booleanos}

        return render_template(
    "dashboard.html",
    df=df.to_html(classes="table", index=False),
    stats=stats,
    fraud_counts=fraud_counts,
    distances=distances,
    labels=labels,
    repeat_counts=pizzas['repeat_retailer'],
    chip_counts=pizzas['used_chip'],
    pin_counts=pizzas['used_pin_number'],
    online_counts=pizzas['online_order']
)

    else:
        return "Nenhuma predição realizada ainda."

@app.route("/predict", methods=["POST"])
def predict():
    if request.is_json:
        dados = request.get_json()
    else:
        dados = request.form.to_dict()

    dados_processados = processar_dados(dados)
    predicao = model.predict([dados_processados])[0]

    # Armazenar no banco
    conn = sqlite3.connect('app/predicoes.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO predicoes (
            distance_from_home,
            distance_from_last_transaction,
            ratio_to_median_purchase_price,
            repeat_retailer,
            used_chip,
            used_pin_number,
            online_order,
            predicao
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (*dados_processados, int(predicao)))
    conn.commit()
    conn.close()

    if request.is_json:
        return jsonify({"predicao": int(predicao)})
    else:
        return redirect(url_for("dashboard"))
