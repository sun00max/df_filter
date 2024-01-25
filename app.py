import datetime
import json
from functools import wraps

import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from flask import (
    Flask,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)

from utils import generate_test_df

app = Flask(__name__)
app.debug = True

# Hard-coded user credentials
VALID_USERS = {"testuser": "password123"}
# jwt token expire duration
EXPIRE_DURATION = 60  # Minutes

# Generate RSA keys for JWT signing
private_key = rsa.generate_private_key(
    public_exponent=65537, key_size=2048, backend=default_backend()
)
public_key = private_key.public_key()

# Generate sample df and set date as index
data_source = generate_test_df()
data_source = data_source.set_index("date")

# Function to generate JWT token
def generate_jwt_token(username):
    """Generate JWT Token with expiration duration"""
    payload = {
        "user": username,
        "exp": datetime.datetime.now(tz=datetime.timezone.utc)
        + datetime.timedelta(minutes=EXPIRE_DURATION),
    }
    token = jwt.encode(payload, private_key, algorithm="RS256")
    # token = jwt.encode(payload, "secret", algorithm="HS256")
    return token


# Login endpoint
@app.route("/login", methods=["POST"])
def login():
    """Verify username and password and return JWT Token"""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username in VALID_USERS and VALID_USERS[username] == password:
        jwt_token = generate_jwt_token(username)
        return jwt_token
    else:
        return jsonify({"error": "Invalid credentials"}), 401


# decorator which valicates JWT Token
def check_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization") or request.form.get("auth")
        if not token:
            return jsonify({"error": "Invalid token"}), 401
        try:
            payload = jwt.decode(token, public_key, algorithms=["RS256"])
            # payload = jwt.decode(token, "secret", algorithms=["HS256"])
            kwargs["user"] = payload["user"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired. Login to refresh token."}), 401
        except jwt.InvalidTokenError as err:
            print(err)
            return jsonify({"error": "Invalid token"}), 401
        return func(*args, **kwargs)
    return wrapper


# Filter data with query
def filter_data(query_params: dict):
    """Filter data with given query conditions"""
    date_filter = query_params.get("date", {})
    numerical_filter = {
        k: v for k, v in query_params.items() if k.startswith("numerical")
    }
    categorical_filter = {
        k: v for k, v in query_params.items() if k.startswith("categorical")
    }
    print(f"sunhq: {date_filter=}, {numerical_filter=}, {categorical_filter=}")
    query_list = []
    # Date filter
    if "late" in date_filter:
        query_list.append(f"index > '{date_filter['late']}'")
    if "before" in date_filter:
        query_list.append(f"index < '{date_filter['before']}'")
    # Numerical filter
    for filter_key, filter_value in numerical_filter.items():
        if "greater equal" in filter_value:
            query_list.append(f"{filter_key} >= {filter_value['greater equal']}")
        if "less equal" in filter_value:
            query_list.append(f"{filter_key} <= {filter_value['less equal']}")
    # Categorical filter
    for filter_key, filter_value in categorical_filter.items():
        query_list.append(f"{filter_key} in {filter_value}")

    query_str = " & ".join(query_list)
    if not query_str:
        res_df = data_source
    else:
        res_df = data_source.query(query_str)
    return res_df


@app.route("/query_api", methods=["POST"])
@check_auth
def query_api(*args, **kwargs):
    """Return filtered data in json format"""
    try:
        query_params = request.get_json()
        if isinstance(query_params, str):
            query_params = json.loads(query_params)
        res_df = filter_data(query_params)
        return jsonify({"results": res_df.to_json()})
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/query", methods=["POST"])
@check_auth
def query(*args, **kwargs):
    """Return filtered data as csv file"""
    filter_payload = request.form.get("filter")
    if not filter_payload:
        filter_payload = {}
    if isinstance(filter_payload, str):
        filter_payload = json.loads(filter_payload)
    res_df = filter_data(filter_payload)

    resp = make_response(res_df.to_csv(chunksize=1000))
    resp.headers[
        "Content-Disposition"
    ] = f"attachment; filename=filtered_data_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp


@app.route("/")
def home():
    return redirect(url_for("index"))


@app.route("/index")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
