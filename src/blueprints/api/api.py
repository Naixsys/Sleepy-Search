from flask import (
        Blueprint,
        render_template,
        request,
        url_for,
        redirect,
        session
)

from utils.account import make_account, update_account, load_account, Account

api = Blueprint('api', __name__, url_prefix='/api')

#@api.route("/", methods=['POST'])




