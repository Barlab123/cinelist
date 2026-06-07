from pathlib import Path

from flask import Flask, jsonify, send_from_directory

from api.routes import api
from db.init import (
    init_db_command_init,
    seed_db_comand_init,
    download_data_command_init,
)

BASE_DIR = Path(__file__).resolve().parent
CLIENT_DIST = BASE_DIR / "client" / "dist"

app = Flask(
    __name__,
    static_folder=str(CLIENT_DIST),
    static_url_path="",
)

app.config["SECRET_KEY"] = "dev-secret-change-me"

app.register_blueprint(api, url_prefix="/api")

init_db_command_init(app)
seed_db_comand_init(app)
download_data_command_init(app)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    if path.startswith("api"):
        return jsonify({"error": "API route not found"}), 404

    requested_file = CLIENT_DIST / path

    if path and requested_file.exists() and requested_file.is_file():
        return send_from_directory(CLIENT_DIST, path)

    index_file = CLIENT_DIST / "index.html"

    if index_file.exists():
        return send_from_directory(CLIENT_DIST, "index.html")

    return jsonify({
        "error": "React build not found. Run: cd client && npm run build"
    }), 500


if __name__ == "__main__":
    app.run(debug=True)