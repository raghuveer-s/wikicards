import os

from flask import Flask

from . import path


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    @app.route("/")
    def hello():
        return "Hello World"

    @app.route("/article/<id>")
    def get_article(id):
        return "Article {}".format(id)
    
    @app.route("/search", methods = ['POST'])
    def search_path(first_url:str, second_url:str):
        return path.find_path(first_url, second_url)

    return app