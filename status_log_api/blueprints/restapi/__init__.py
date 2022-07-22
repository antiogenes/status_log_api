#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Blueprint, abort, jsonify, make_response

from status_log_api.service import getStatusJobs

from status_log_api.ratelimiter import limiter


api_bp = Blueprint('restapi', __name__, url_prefix='/api/v1')
limiter.limit("10/minute")(api_bp)


@api_bp.route('/status/<string:namespace>/<string:projeto>')
def get(namespace, projeto):
    status = getStatusJobs(namespace=namespace, projeto=projeto) or abort(404)
    return jsonify(status)


@api_bp.errorhandler(429)
def too_many_requests(error):
    return make_response(jsonify({'message': u'Excedeu o limite de requisições por minuto'}), 200) # noqa


@api_bp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': u'URL não encontrada'}), 404)


def init_app(app):
    app.register_blueprint(api_bp)
