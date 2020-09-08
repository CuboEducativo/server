import json
import random

import requests
from flask import Flask, request
from flask_cors import CORS
from uuid import uuid1

import setup
from params import SPREADSHEET_ID, PORT, HOST, FLOW_API_KEY, API_URL
from helpers import matrix_to_df, signParams

app = Flask(__name__)
CORS(app)

service = setup.init_service()

# Call the Sheets API
sheet = service.spreadsheets()

def generate_payment(numbers):
    params = {
        'apiKey': FLOW_API_KEY,
        'commerceOrder': 'rifa2020-{}'.format(uuid1()),
        'subject': 'test',
        'amount': '{}'.format(len(numbers) * 1000),
        'email': 'mail@example.org',
        'urlConfirmation': '{}/paymentCallback'.format(API_URL),
        'urlReturn': 'https://google.com',
        'optional': json.dumps({
            'numbers': json.dumps([2,10])
        })
    }
    params['s'] = signParams(params)
    response = requests.post('https://www.flow.cl/api/payment/create', data = params)
    response = response.json()
    print(response)
    params = {
        'apiKey': FLOW_API_KEY,
        'token': response['token']
    }
    params['s'] = signParams(params)
    status = requests.get('https://www.flow.cl/api/payment/getStatus', params=params)
    status = status.json()
    print(status)
    return response

def reserve_numbers(numbers):
    for number in numbers:
        body = { 
        "values": [[ 1 ]]
        }
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range='Rifa!B{}'.format(number+1),
            valueInputOption="RAW",
            body=body
        ).execute()

@app.route('/')
def hello_world():
    return generate_payment()
    # result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
    #                             range='Dashboard').execute()
    # values = result.get('values', [])

    # return matrix_to_df(values).to_dict()


@app.route('/paymentCallback', methods=['POST', 'GET'])
def payment():
    # request.get_json(force=True)['numbers']
    token = request.values.to_dict(flat=False)['token']

    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID, range='TEST',
        valueInputOption='RAW', body=body).execute()
    return data


@app.route('/rifaNumeros')
def rifa():
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range='Rifa').execute()
    values = result.get('values', [])
    df = matrix_to_df(values)
    df = df[df['Estado'] == '0']
    return {
        'available': df['Numero'].tolist()
        }

@app.route('/buyNumbers', methods=['POST'])
def buy_numbers():
    numbers = request.get_json(force=True)['numbers']
    reserve_numbers(numbers)
    generate_payment(numbers)
    return 'done'

if __name__ == '__main__':
    app.run(threaded=True, host=HOST, port=PORT)