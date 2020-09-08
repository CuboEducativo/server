import os
from environs import Env

# read enviroment
env = Env()
env.read_env()

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = env.str("SPREADSHEET_ID")
PORT = int(os.environ.get('PORT', 8080))
HOST = os.environ.get('HOST', '0.0.0.0')

# Flow secret key
FLOW_SECRET_KEY = env.str("FLOW_SECRET_KEY")
FLOW_API_KEY = env.str("FLOW_API_KEY")

# THIS API URL
API_URL = env.str("API_URL")