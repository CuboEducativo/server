import json
import random

import requests
from flask import Flask, request
from flask_cors import CORS
from uuid import uuid1

from setup import sheets
from params import SPREADSHEET_ID, PORT, HOST, FLOW_API_KEY, API_URL
from helpers import matrix_to_df, signParams
from rifa import generate_payment, reserve_numbers, takeNumbers, get_payment_status

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return ''
    # result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
    #                             range='Dashboard').execute()
    # values = result.get('values', [])

    # return matrix_to_df(values).to_dict()


@app.route('/paymentCallback', methods=['POST', 'GET'])
def payment():
    token = request.values.to_dict(flat=False)['token'][0]
    status = status = get_payment_status(token)
    numbers = status['optional']['numbers']
    takeNumbers(numbers)
    return 'done'


@app.route('/rifaNumeros')
def rifa():
    result = sheets.values().get(spreadsheetId=SPREADSHEET_ID,
                                range='Rifa').execute()
    values = result.get('values', [])
    df = matrix_to_df(values)
    df = df[df['Estado'] == '0']
    return {
        'available': df['Numero'].tolist()
        }

@app.route('/buyNumbers', methods=['POST'])
def buy_numbers():
    data = request.get_json(force=True)
    numbers = data['numbers']
    email = data['email']
    instagram = data['instagram']
    address = data['address']

    result = reserve_numbers(numbers, email, instagram, address)
    if result['action'] == 'not_reserved':
        return result
    payment = generate_payment(numbers, email)

    return {
        'action': 'reserved',
        'payment_url': '{}?token={}'.format(payment['url'],payment['token'])
    }

if __name__ == '__main__':
    app.run(threaded=True, host=HOST, port=PORT)