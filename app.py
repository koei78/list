from flask import Flask
from dotenv import load_dotenv

from src.db import init_db
from src.routes import register_routes


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",  # override with env var in production
    )

    init_db()
    register_routes(app)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
