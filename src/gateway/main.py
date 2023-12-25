import os

import yaml
from flask import Flask

from routes.gateway_routes import gateway_app
from routes.library_routes import library_app
from routes.rating_routes import rating_app
from routes.reservation_routes import reservation_app


def load_config(app: Flask, config_path: str):
    with open(config_path, "r") as config_file:
        config_yaml = yaml.safe_load(config_file)
    app.config.update(
        port=config_yaml["server"]["port"],
        host=config_yaml["server"].get("host", "0.0.0.0"),
    )
    for service in config_yaml["services"]:
        for key in service.keys():
            service_name = key
            hostname = service[key]["hostname"]
            port = service[key]["port"]
            url = f"http://{hostname}:{port}"
            app.config[service_name] = url


def create_app(config_filename):
    app = Flask(__name__)

    load_config(app, config_filename)
    app.json.sort_keys = False

    app.register_blueprint(gateway_app)
    app.register_blueprint(library_app)
    app.register_blueprint(rating_app)
    app.register_blueprint(reservation_app)

    return app


if __name__ == '__main__':
    if os.getenv("local-dev"):
        config_file = "config_local.yaml"
    else:
        config_file = "config.yaml"
    app = create_app(config_file)
    app.run(host=app.config.get("host"), port=app.config.get("port"))
