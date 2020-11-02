from flask import Flask


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

    return app