from flask import Flask, jsonify
from lucratividade import Lucratividade
import json
app = Flask(__name__)

@app.route('/api')
def api():
    lc = Lucratividade(comissao=1, data_inicial='2023-03-27', data_final='2023-03-27').lucratividade_por_item
    return lc

if __name__ == '__main__':
    app.run(debug=True)
