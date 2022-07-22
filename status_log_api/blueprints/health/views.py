from flask import jsonify


def index():
    """
    Check health status..
    """
    return jsonify({'status': 200})
