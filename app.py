from flask import Flask, g
from api.routes import api
from web.routes import web
from db.init import init_db_command_init, seed_db_comand_init
import secrets

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(web)
init_db_command_init(app)
seed_db_comand_init(app)

if __name__ == "__main__":
    app.run(debug=True)