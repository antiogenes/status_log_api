#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, make_response

from .views import index

health_bp = Blueprint("health", __name__)

health_bp.add_url_rule("/health", view_func=index)


@health_bp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': u'URL não encontrada'}), 404)


def init_app(app):
    app.register_blueprint(health_bp)
