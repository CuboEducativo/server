import hmac
import hashlib

import pandas as pd
import numpy as np

from params import FLOW_SECRET_KEY

def matrix_to_df(matrix):
    columns, *rest = matrix
    d = {}
    values = np.array(rest)

    for i, column in enumerate(columns):
        d[column] = values[:,i]

    return pd.DataFrame(d)

def stringToSign(dictionary):
  string = ""
  for key in sorted(dictionary.keys()):
    string += key + dictionary[key]
  return string

def signParams(params):
  message = stringToSign(params)
  signature = hmac.new(
    bytes(FLOW_SECRET_KEY , 'latin-1'),
    msg = bytes(message , 'latin-1'),
    digestmod = hashlib.sha256
    ).hexdigest()
  return signature