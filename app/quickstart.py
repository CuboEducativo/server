from flask import Flask

import setup
from params import SPREADSHEET_ID, PORT, HOST
from helpers import matrix_to_df

app = Flask(__name__)

service = setup.init_service()

# Call the Sheets API
sheet = service.spreadsheets()

@app.route('/')
def hello_world():
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range='Dashboard').execute()
    values = result.get('values', [])
    return matrix_to_df(values).to_dict()

if __name__ == '__main__':
    app.run(threaded=True, host=HOST, port=PORT)