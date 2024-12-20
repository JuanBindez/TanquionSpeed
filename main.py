from flask import Flask, render_template, request, jsonify
import speedtest
import json
import time

app = Flask(__name__)

# Configuração do speedtest
st = speedtest.Speedtest()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/speedtest', methods=['GET'])
def speedtest_route():
    # Realiza o speedtest
    st.get_servers()
    st.get_best_server()
    st.download()
    st.upload()
    results_dict = st.results.dict()

    # Converte os resultados para JSON
    results_json = json.dumps(results_dict)

    # Retorna os resultados em formato JSON
    return jsonify(results_json)

if __name__ == '__main__':
    app.run(debug=True)