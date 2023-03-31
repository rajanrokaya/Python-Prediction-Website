"""
This module is the entry point of the application.

The 'flask' module is imported because the code is using Flask, a web
framework for Python, to build the application.
"""

from flask import Flask


def create_app():
    """
    This function creates and configures an instance of a Flask app and
    register blueprints for different functionality in the application

    :return: The Flask app instance
    """

    app = Flask(__name__)

    from website.home import views
    from website.datas import datas
    from website.graph_bar import graph_bar
    from website.graph_line import graph_line

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(datas, url_prefix='/')
    app.register_blueprint(graph_bar, url_prefix='/')
    app.register_blueprint(graph_line, url_prefix='/')

    return app



