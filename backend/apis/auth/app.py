"""Python Flask WebApp Auth0 integration example
"""

import json
import os
from os import environ as env
from requests import post
from urllib.parse import quote_plus, urlencode
from middleware.auth_middleware import validate_access_token
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for
from middleware.auth_middleware import validate_access_token


API_URL = f"{os.environ['API_URL']}"
USERS_URL = f"{API_URL}/user"

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

FRONTEND_URL = os.environ["FRONTEND_URL"]
oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)


# Controllers API
@app.route("/")
def home():
    return render_template(
        "home.html",
        redirect=FRONTEND_URL,
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


@app.route("/callback", methods=["GET", "POST"])
def callback():
    """sets token and calls user table"""
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    user_info = token["userinfo"]
    uid, username, email = user_info["sub"], user_info["nickname"], user_info["email"]
    create_user(uid, username, email)
    return redirect("/")


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True),
        audience="https://dev-eym6ylpoplxr2f0n.jp.auth0.com/api/v2/"
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


@app.route("/secret")
@validate_access_token
def secret_fn(decoded_token):
    """tests protected route"""
    return decoded_token


def create_user(uid: str, username: str, email: str) -> None:
    """creates user"""
    create_user_route = f"{USERS_URL}/{uid}"
    post(create_user_route, json={
        "username": username, "email": email}, timeout=5000)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))
