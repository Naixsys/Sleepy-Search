from flask import Flask

from blueprints import pages, api
import config
from utils.database import get_db_connection, init_db

app = Flask(__name__, template_folder=config.template_folder, static_folder=config.static_folder)
app.secret_key = config.secret_key
app.config['MAX_CONTENT_LENGHT'] = config.max_file_size

app.register_blueprint(pages)
app.register_blueprint(api)

with app.app_context():
    init_db()
    get_db_connection()

if __name__ == "__main__":
    app.run(debug=config.development_mode)
