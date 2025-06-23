# matrices.py
from flask import Blueprint, request, jsonify
import numpy as np
from scipy.stats import pearsonr, spearmanr, kendalltau
from fastdtw import fastdtw

matrices_bp = Blueprint('matrices', __name__)

@matrices_bp.route('/api/compare', methods=['POST'])
def compare_series():
    """
    Compute agreement metrics between two time series.
    Expects JSON: { "seriesA": [float,...], "seriesB": [float,...] }

    Returns JSON with:
      - pearson_r
      - spearman_rho
      - kendall_tau
      - dtw   (dynamic time warping distance)
      - mse   (mean squared error, optional)
    """
    data = request.get_json(force=True)
    a = np.array(data.get('seriesA', []), dtype=float)
    b = np.array(data.get('seriesB', []), dtype=float)

    # Validate input lengths
    if a.size == 0 or b.size == 0:
        return jsonify({"error": "Empty series"}), 400
    if a.shape != b.shape:
        return jsonify({"error": "Series length mismatch"}), 400

    # Pearson correlation
    pearson_r, _ = pearsonr(a, b)

    # Spearman correlation
    spearman_rho, _ = spearmanr(a, b)

    # Kendall's tau
    kendall_tau, _ = kendalltau(a, b)

    # Mean Squared Error
    mse = float(np.mean((a - b) ** 2))

    # Dynamic Time Warping distance
    dtw_dist, _ = fastdtw(a, b)

    return jsonify({
        'pearson_r': pearson_r,
        'spearman_rho': spearman_rho,
        'kendall_tau': kendall_tau,
        'mse': mse,
        'dtw': float(dtw_dist)
    })