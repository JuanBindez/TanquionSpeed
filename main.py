from flask import Flask, render_template, jsonify
import json
import speedtest  # Certifique-se de instalar o módulo speedtest-cli com `pip install speedtest-cli`
import requests

app = Flask(__name__)

@app.route('/speedtest', methods=['GET'])
def speedtest_route():
    # Realiza o speedtest
    st = speedtest.Speedtest()
    st.get_servers()
    st.get_best_server()
    download_speed = st.download() / 1_000_000  # Convertendo para Mbps
    upload_speed = st.upload() / 1_000_000  # Convertendo para Mbps
    ping = st.results.ping

    # Organizando os resultados
    results_dict = {
        "download": download_speed,
        "upload": upload_speed,
        "ping": ping,
        "server": st.results.server,
        "client": st.results.client,
        "timestamp": st.results.timestamp
    }

    # Retorna os resultados em formato JSON
    return jsonify(results_dict)


@app.route('/')
def index():
    # Faz uma requisição à rota '/speedtest' para pegar os dados
    response = requests.get('http://127.0.0.1:5000/speedtest')

    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        data = response.json()

        # Renderiza o template e passa os dados
        return render_template('index.html', download=data['download'], upload=data['upload'], ping=data['ping'], server=data['server'], client=data['client'])
    else:
        return f"Erro ao consumir a API: {response.status_code}"


if __name__ == "__main__":
    app.run(debug=True)
