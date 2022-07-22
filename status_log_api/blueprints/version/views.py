from flask import jsonify
from status_log_api.__init__ import __version__ as version


def index():
    """
    Retorna a versão da aplicação.
    """
    return jsonify({'name': 'big-status-batch-api', 'version': version})
