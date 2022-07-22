#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask

from status_log_api.ext import configuration

from status_log_api.ratelimiter import limiter


def minimal_app(**config):
    app = Flask(__name__)
    configuration.init_app(app, **config)
    return app


def create_app(**config):
    app = minimal_app(**config)
    configuration.load_extensions(app)
    limiter.init_app(app)
    return app
