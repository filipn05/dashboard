# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from data_manager import add_dataset, list_datasets, remove_dataset, get_series
import pandas as pd
import os
from matrices import matrices_bp

app = Flask(__name__)
CORS(app)  # allow requests from your Vue frontend during development

# register the metrics blueprint
app.register_blueprint(matrices_bp)

# — Upload a new dataset —
@app.route('/api/datasets', methods=['POST'])
def upload_dataset():
    f = request.files.get('file')
    if not f:
        return jsonify({'error': 'No file provided'}), 400

    try:
        ds_id, columns = add_dataset(f)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'id': ds_id, 'columns': columns}), 201


# — List all datasets —
@app.route('/api/datasets', methods=['GET'])
def get_datasets():
    return jsonify(list_datasets())


# — Delete a dataset by ID —
@app.route('/api/datasets', methods=['DELETE'])
def delete_dataset():
    data = request.get_json() or {}
    ds_id = data.get('id')
    if not ds_id or ds_id not in list_datasets():
        return jsonify({'error': 'Dataset not found'}), 404

    remove_dataset(ds_id)
    return jsonify({'removed': ds_id})


# — Fetch one series’ x/y data for plotting —
@app.route('/api/series-data', methods=['POST'])
def series_data():
    data = request.get_json() or {}
    ds_id = data.get('dataset')
    col   = data.get('column')

    try:
        y, x = get_series(ds_id, col)
    except KeyError as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'x': x, 'y': y})


if __name__ == '__main__':
    # Runs on http://localhost:5000 by default
    app.run(port=5000, debug=True)
