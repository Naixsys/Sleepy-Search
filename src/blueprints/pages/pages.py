from flask import (
        Blueprint,
        render_template,
        request,
        url_for,
        redirect,
        session,
        make_response,
        flash,
        send_from_directory
)

from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from hashlib import sha512
import os

from utils.account import (
        Account,
        make_account,
        update_account,
        load_account,
)
from utils.post import (
        Post,
        search_posts_by_tag,
        search_post_by_media_id,
        find_post_tags,
        load_post,
        make_post,
        assign_post_tag,
        make_posts_data_props,
        make_post_data_tagged,
        update_post,
        remove_post_all_tags,
        remove_post
)

from utils.tag import (
        Tag,
)

from config import (
        about_us,
        content_folder,
        hash_buffer_size,
        num_preview_tags
)

pages = Blueprint('pages', __name__)

@pages.get("/")
def home():
    props = {
            "user_info" : session['user_info'] if 'user_info' in session else None,
            }
    response = render_template('index.html', props=props)

    return response

@pages.route("/login/", methods=['POST', 'GET'])
def login():

    props = {
            "user_info" : session['user_info'] if 'user_info' in session else None,
            }

    if request.method == 'POST':
        user = request.form["uname"]
        password = request.form["password"]
        user : Account = Account({
                    "account_username": user
                })

        account_info = load_account(user)
        if account_info is not None:
            if password == account_info['account_password']:
                account_info.pop('account_password')
                session['user_info'] = account_info

                props = {
                        'user_info': account_info
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
    props = {
            "user_info" : session['user_info'] if 'user_info' in session else None,
            }
    try:
        if session['user_info']:
            session.pop('user_info')
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
    props = {
            "user_info" : session['user_info'] if 'user_info' in session else None,
            }
    if request.method == 'POST':
        user = request.form["uname"]
        password = request.form["password"]
        # TODO: Fix hardcoded role
        role = 3
        account : Account = Account({
                "account_username": user,
                "account_role": role,
                "account_password": password
                })

        if make_account(account):
            user_info = load_account(account)
            user_info.pop("account_password")
            session['user_info'] = user_info
            props['user_info'] = user_info
            response = redirect(url_for('pages.home'))
        else:
            props['error'] = "Sign-up failed"
            response = render_template('error.html', props=props)

    else:
        response = render_template('signup.html', props=props)

    return response


@pages.route("/dashboard/", methods=['POST', 'GET'])
def dashboard():
    props = {
            "user_info" : session['user_info'] if session['user_info'] else None,
            }
    response = render_template('dashboard.html', props=props)
    return response

@pages.route("/account/", methods=['POST', 'GET', 'DELETE'])
def account():
    props = {
            "user_info" : session['user_info'] if 'user_info' in session else None,
            }
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        current_user: Account = Account({
                    "account_id": session['user_info']['account_id'],
                    "account_username": session['user_info']['account_username']
                })

        old_account_info =  load_account(current_user)
        if old_account_info.account_id:
            new_account_info : Account = Account({
                    "account_id": old_account_info.account_id,
                    "account_role": role,
                    "account_username": username,
                    "account_password": password
                    })
            if update_account(new_account_info):
                session['user_info'] = load_account(new_account_info).pop('account_password')
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
        if 'user_info' in session:
            props = {
                    'user_info' : session['user_info'],
                    }
            response = render_template('account.html', props=props)

        else:
            props = {
                    'error': "Please sign in before accessing this page"
                    }
            response = render_template('error.html', props=props)

    return response

@pages.route("/about/")
def about():
    props = {
            "user_info" : session['user_info'] if 'user_info' in session else None,
            'about_us': about_us
            }

    response = render_template('about.html', props=props)
    return response

@pages.route("/library/")
def library():
    posts: Post = search_posts_by_tag()
    posts = make_posts_data_props(posts, num_preview_tags)

    props = {
            "user_info" : session['user_info'] if 'user_info' in session else None,
            "posts" : posts
            }


    response = render_template('library.html', props=props)
    return response

@pages.route("/contact/")
def contact():
    props = {
            "user_info" : session['user_info'] if 'user_info' in session else None,
            }

    response = render_template('contact.html', props=props)
    return response

@pages.get("/search/")
def search():

    tag : Tag = {
                 "tag_name": request.args.get("search_text").strip().lower()
                 }

    posts = search_posts_by_tag(tag)
    posts = make_posts_data_props(posts, num_preview_tags)
    props = {
            "user_info" : session['user_info'] if 'user_info' in session else None,
            "posts": posts,
            "media_path": content_folder
            }

    response = render_template('library.html', props=props)
    return response

@pages.route("/error/")
def error():

    props = {
            "user_info" : session['user_info'] if 'user_info' in session else None,
            }
    response = render_template('error.html', props=props)
    return response

@pages.route("/modify_post/<post_id>", methods=['POST', 'GET'])
def modify_post(post_id: int):
    post : Post = load_post({"post_id": post_id})
    if post:
        if request.method == "GET":
            props = {
                "user_info" : session['user_info'] if 'user_info' in session else None,
                "post": make_post_data_tagged(post)
                }

            response = render_template('edit-post.html', props=props)
            return response

        elif request.method == "POST":
            tags = request.form["tags"]
            description = request.form["description"]
            if description:
                post['post_description'] = description
                update_post(post)

            # TODO: Fix hardcoded tag namespace
            remove_post_all_tags(post)
            tags: list[Tag] = [ {"tag_name": tag.lower().strip(), "tag_namespace": "content" } for tag in tags.split(',') ]
            for tag in tags:
                assign_post_tag(post, tag)

            response = redirect(url_for('pages.modify_post', post_id=post['post_id']))

    else:

        props= {
                'error': f"Post ID: {post_id} does not exist"
                }
        response = render_template('error.html', props=props)

    return response
@pages.route("/delete_post/<post_id>", methods=["POST"])
def delete_post(post_id):
    if(remove_post({"post_id": post_id})):
        response = redirect(url_for('pages.library'))
    else:
        props= {
                'error': f"Error deleting post with ID: {post_id}"
                }
        response = render_template('error.html', props=props)

    return response

@pages.route("/new_post", methods=['POST'])
def new_post():
    uploaded_file = request.files['file']
    tags = request.form['tags']
    description = request.form['description']
    post_creator_id = session['user_info']['account_id']

    try:
        if uploaded_file:
            file_hash = sha512()
            file_data = b''
            while True:
                data = uploaded_file.read(hash_buffer_size)
                file_data += data
                if not data:
                    break
                file_hash.update(data)

            final_hash = file_hash.hexdigest()

            with open(os.path.join(content_folder, secure_filename(final_hash)), 'wb') as file:
                file.write(file_data)

            post : Post = {
                        "post_creator_id": post_creator_id,
                        "post_media_id": final_hash,
                        "post_description": description,

                    }

            if make_post(post):
                post = search_post_by_media_id(post)
                # TODO: Fix hardcoded tag namespace
                tags: list[Tag] = [ {"tag_name": tag.lower().strip(), "tag_namespace": "content" } for tag in tags.split(',') ]
                for tag in tags:
                    assign_post_tag(post, tag)

                response = redirect(url_for("pages.home"))
                return response

        else:
            response = make_response("Please select a file to upload", 400)
            return response

    except RequestEntityTooLarge:
        response = make_response("Uploaded file exceeds file size limit.", 413)

@pages.get("/file/<file_id>")
def serve_file(file_id):
    return send_from_directory(content_folder, file_id)
