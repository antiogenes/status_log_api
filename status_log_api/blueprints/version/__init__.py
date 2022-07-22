#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, make_response

from .views import index

version_bp = Blueprint("version", __name__)

version_bp.add_url_rule("/", view_func=index)


@version_bp.errorhandler(429)
def too_many_requests(error):
    return make_response(jsonify({'error': u'Excedeu o limite de requisições por minuto'}), 429) # noqa


@version_bp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': u'URL não encontrada'}), 404)


def init_app(app):
    app.register_blueprint(version_bp)
