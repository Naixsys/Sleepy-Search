from flask import (
        Blueprint,
        render_template,
        request,
        url_for,
        redirect,
        session
)

from utils.account import make_account, update_account, load_account, Account

pages = Blueprint('pages', __name__)

@pages.get("/")
def home():
    props = {}
    if 'user' in session:
        props = {
        'user': session['user']
        }
    response = render_template('index.html', props=props)

    return response

@pages.route("/login/", methods=['POST', 'GET'])
def login():
    props = {}
    if 'user' in session:
        props = {
        'user': session['user']
        }

    if request.method == 'POST':
        user = request.form["username"]
        password = request.form["password"]
        account_info = load_account(user)
        if account_info is not None:
            if password == account_info.password_hash:
                session['user'] = user
                session['role'] = account_info.role
                props = {
                        'user': user
                        }
                response = redirect(url_for('pages.home'))

            else:

                props= {
                        'error': f"Wrong password for user: {user}"
                       }

                response = render_template('error.html', props=props)
        else:
                props= {
                        'error': f"The specified user: {user} does not exist"
                        }
                response = render_template('error.html', props=props)


    else:
        response = render_template('login.html', props=props)

    return response

@pages.get("/logout/")
def logout():
    props = {}
    try:
        if session['user']:
            session.pop('user')
            response = redirect(url_for('pages.home'))
        else:
            props['error'] = "You are not logged in....therefore you cannot logout"
            response = render_template('error.html', props=props)

    except:
        props['error'] = "Error during logout"
        response = render_template('error.html', props=props)

    return response

@pages.route("/signup/", methods=['POST', 'GET'])
def signup():
    props = {}
    if request.method == 'POST':
        user = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        account = Account(None, role, user, password)
        if make_account(account):
            session['user'] = user
            session['role'] = role
            props['user'] = user
            props['role'] = role
            response = redirect(url_for('pages.home'))
        else:
            props['error'] = "Sign-up failed"
            response = render_template('error.html', props=props)

    else:
        response = render_template('signup.html', props=props)

    return response


@pages.route("/dashboard/", methods=['POST', 'GET'])
def dashboard():
    return response

@pages.route("/account/", methods=['POST', 'GET', 'DELETE'])
def account():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        current_user = session['user']
        old_account_info =  load_account(current_user)
        if old_account_info.account_id:
            new_account_info = Account(old_account_info.account_id, role, username, password)
            if update_account(new_account_info):
                session['user'] = username
                session['role'] = role
                response = redirect(url_for('pages.account'))
            else:
                props = {
                        'error': f"Failed to change user details"
                        }
                response = render_template('error.html', props=props)
        else:
            props = {
                    'error': f"user {current_user} does not exist"
                    }
            response = render_template('error.html', props=props)

    elif request.method == "DELETE":
        pass

    else:
        if 'user' in session:
            props = {
                    'user' : session['user'],
                    }
            response = render_template('account.html', props=props)

        else:
            props = {
                    'error': "Please sign in before accessing this page"
                    }
            response = render_template('error.html', props=props)

    return response

@pages.route("/error/")
def error():
    response = render_template('error.html', props=props)
    return response
