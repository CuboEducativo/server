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
        'subject': 'Numero de rifa',
        'amount': '{}'.format(len(numbers) * 1000),
        'email': '{}'.format(email),
        'urlConfirmation': '{}/paymentCallback'.format(API_URL),
        'urlReturn': 'https://www.cuboeducativo.cl/gracias',
        'optional': json.dumps({
            'numbers': json.dumps(numbers)
        })
    }
    params['s'] = signParams(params)
    response = requests.post('https://www.flow.cl/api/payment/create', data = params)
    return response.json()


def takeNumbers(numbers):
    for number in numbers:
        body = { 
        "values": [[ NumberStatus.TAKEN.value ]]
        }
        result = sheets.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range='Rifa!B{}'.format(number+1),
            valueInputOption="RAW",
            body=body
        ).execute()


def reserve_numbers(numbers, email = '', instagram = '', address = ''):
    result = sheets.values().get(spreadsheetId=SPREADSHEET_ID,
                               range='Rifa').execute()
    values = result.get('values', [])
    df = matrix_to_df(values)
    strNumbers = [str(i) for i in numbers]
    numbers_df = df[df['Numero'].isin(strNumbers)]
    unavailable = numbers_df[numbers_df['Estado'] != '0']
    if unavailable.shape[0] == 0:
        for number in numbers:
            body = { 
            "values": [[ NumberStatus.RESERVED.value, email, address, instagram ]]
            }
            result = sheets.values().update(
                spreadsheetId=SPREADSHEET_ID,
                range='Rifa!B{}:E{}'.format(number+1,number+1),
                valueInputOption="RAW",
                body=body
            ).execute()
        return {
            'action': 'reserved'
        }
    else:
        return {
            'action': 'not_reserved',
            'not_available': unavailable['Numero'].tolist()
        }

