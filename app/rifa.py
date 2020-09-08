import json
import random
from enum import Enum

import requests
from flask import Flask, request
from flask_cors import CORS
from uuid import uuid1

from params import SPREADSHEET_ID, FLOW_API_KEY, API_URL
from helpers import matrix_to_df, signParams
from setup import sheets

class NumberStatus(Enum):
  AVAILABLE = 0
  RESERVED = 1
  TAKEN = 2

def get_payment_status(token):
    params = {
        'apiKey': FLOW_API_KEY,
        'token': token
    }
    params['s'] = signParams(params)
    status = requests.get('https://www.flow.cl/api/payment/getStatus', params=params)
    return status.json()

def generate_payment(numbers, email):
    params = {
        'apiKey': FLOW_API_KEY,
        'commerceOrder': 'rifa2020-{}'.format(uuid1()),
        'subject': 'Números de rifa',
        'amount': '{}'.format(len(numbers) * 1000),
        'email': email,
        'urlConfirmation': '{}/paymentCallback'.format(API_URL),
        'urlReturn': 'https://google.com',
        'optional': json.dumps({
            'numbers': json.dumps(numbers)
        })
    }
    params['s'] = signParams(params)
    response = requests.post('https://www.flow.cl/api/payment/create', data = params)
    response = response.json()
    print(response)
    return response

def write_numbers(numbers, value):
    for number in numbers:
        body = { 
        "values": [[ value ]]
        }
        result = sheets.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range='Rifa!B{}'.format(number+1),
            valueInputOption="RAW",
            body=body
        ).execute()

def reserve_numbers(numbers):
    write_numbers(numbers, NumberStatus.RESERVED.value)

