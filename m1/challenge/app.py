import os
import jwt
from flask import Flask, Response, render_template, request, make_response
from typing import Dict, Union


app = Flask(__name__)

# The challenge is that you have to figure this out to get the flag.
PASSWORD: str = os.getenv(
    "SECRET", "NOT_REAL_SECRET"
)
FLAG = os.getenv("FLAG", "CS2107{FAKE_FLAG_DO_NOT_SUBMIT}")
JWT_TYPE = Dict[str, Union[str, bool]]
DEFAULT_TOKEN = {"admin": False}
TOKEN_NAME = "auth_token"
ALGORITHM = "HS256"


def encode_jwt(data: JWT_TYPE) -> str:
    """Encode Dict to JWT"""
    return jwt.encode(data, PASSWORD, ALGORITHM)


def decode_jwt(jwt_token: str) -> JWT_TYPE:
    """Decode JWT into Dict"""
    return jwt.decode(jwt_token, PASSWORD, ALGORITHM)


JWT_DEFAULT_TOKEN = encode_jwt(DEFAULT_TOKEN)


@app.route("/")
def index() -> Response:
    """The main website for the challenge"""
    raw_cookie = request.cookies.get(TOKEN_NAME, JWT_DEFAULT_TOKEN)
    auth_token = decode_jwt(raw_cookie)

    if auth_token.get("admin"):
        return render_template("flag.html", flag=FLAG)

    response = make_response(render_template("index.html"))
    response.set_cookie(TOKEN_NAME, encode_jwt(auth_token))

    return response


if __name__ == "__main__":
    # Do not do this in prod.
    app.run(debug=True)
