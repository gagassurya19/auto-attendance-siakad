from googleapiclient.discovery import build
from google.oauth2 import service_account


SERVICE_ACCOUNT_FILE = './account/key.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = ''
RANGE_DATA = "Sheet1!A:B"

def getaccount():
	creds = service_account.Credentials.from_service_account_file(
			SERVICE_ACCOUNT_FILE, scopes=SCOPES)
	service = build('sheets', 'v4', credentials=creds)

	sheet = service.spreadsheets()
	result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
										range=RANGE_DATA).execute()

	values = result.get('values', [])
	return values