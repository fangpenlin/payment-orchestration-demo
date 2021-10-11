import os
import requests
from flask import Flask
from flask import render_template, request
from flask import request
from flask_cors import CORS

app = Flask(__name__)
auth_api = "https://auth.verygoodsecurity.com/auth/realms/vgs/protocol/openid-connect/token"

TNT_ID = os.environ.get('TNT_ID')

CORS(app)

def get_access_token():
    data = {
        'client_id': os.environ.get('MULTIPLEXING_AUTH_ID'),
        'client_secret': os.environ.get('MULTIPLEXING_AUTH_SECRET'),
        'grant_type': 'client_credentials',
    }
    response = requests.post(auth_api, data=data)
    return response.json()
        
@app.route("/")
def index():
    access_token = get_access_token()
    return render_template('./index.html', tnt=TNT_ID, accessToken=access_token['access_token'])

@app.route("/transfers", methods=['POST'])
def transfer():
    req = request.get_json()
    access_token = get_access_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(access_token['access_token'])
    }
    transfers_data = {
        "amount": 1 * 100,
        "currency": "USD",
        "source": req['finantial_instrument'],
    }
    tr = requests.post('https://{}.sandbox.verygoodproxy.com/transfers'.format(TNT_ID),
        headers=headers,
        json=transfers_data
    )
    return tr.json()
