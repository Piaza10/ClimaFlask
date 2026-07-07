from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/clima', methods=['POST'])
def clima():
    cidade = request.form['cidade']
    print("Cidade recebida:", cidade)

    api_key = os.getenv('WEATHER_API_KEY')

    url = "https://api.weatherapi.com/v1/current.json"

    params = {
        "key": api_key,
        "q": cidade,
        "lang": "pt"
    }

    resposta = requests.get(url, params=params)
    dados = resposta.json()

    print("Status:", resposta.status_code)
    print("Resposta:", dados)

    if resposta.status_code == 200:
        location = dados.get("location")
        current = dados.get("current")
        
        if not location or not current:
            return render_template("resultado.html", erro="Não foi possível ver os dados do clima. Tente novamente.")
        
        condition = current.get("condition")
        if not condition:
            return render_template("resultado.html", erro="Não foi possível ver os dados do clima. Tente novamente")


        clima_dados = {
            "cidade": cidade,
            "temperatura": current.get("temp_c", "Indisponível"),
            "umidade": current.get("humidity", "Indisponível"),
            "descricao": condition.get("text", "Indisponível")
        }

        return render_template('resultado.html', clima=clima_dados)
    else:
        return render_template('resultado.html', erro="Cidade não encontrada ou API Key inválida.")



if __name__ == "__main__":
    app.run(debug=True)