import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from flask import Flask, request, jsonify
from flask_cors import CORS
import inventory_tools

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/stock', methods=['GET'])
def get_stock():
    product_id = request.args.get('product_id')
    if not product_id:
        return jsonify({'error': 'product_id required'}), 400
    val = inventory_tools.get_stock(product_id)
    if val is None:
        return jsonify({'product_id': product_id, 'stock': 0})
    return jsonify({'product_id': product_id, 'stock': val})

@app.route('/api/stock', methods=['POST'])
def update_stock():
    j = request.get_json() or {}
    product_id = j.get('product_id')
    delta = j.get('delta')
    if product_id is None or delta is None:
        return jsonify({'error': 'product_id and delta required'}), 400
    try:
        delta = int(delta)
    except ValueError:
        return jsonify({'error': 'delta must be an integer'}), 400
    new = inventory_tools.update_stock(product_id, delta)
    return jsonify({'product_id': product_id, 'stock': new})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
