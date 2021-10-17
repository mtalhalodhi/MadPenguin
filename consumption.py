import gspread
from oauth2client.service_account import ServiceAccountCredentials
import telegram
import os

def get_unseen_by_user(telegram_username):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(generate_google_creds_dict(), scope)
    client = gspread.authorize(creds)
    name_on_sheet = get_name_by_telegram_user(telegram_username, client)

    shows_list_worksheet = client.open_by_key(get_key_for_spreadsheet()).worksheet("Consumption Queue")
    filtered_records = list(filter(lambda record : (record[name_on_sheet] == "No"),shows_list_worksheet.get_all_records()))

    unseen_telegram_message = ""
    for filtered_json in filtered_records:
        unseen_telegram_message += record_to_message_format(filtered_json)
    return unseen_telegram_message

def generate_google_creds_dict():
    variables_keys = {
        "type": os.getenv("SHEET_TYPE"),
        "project_id": os.getenv("SHEET_PROJECT_ID"),
        "private_key_id": os.getenv("SHEET_PRIVATE_KEY_ID"),
        "private_key": os.getenv("SHEET_PRIVATE_KEY"),
        "client_email": os.getenv("SHEET_CLIENT_EMAIL"),
        "client_id": os.getenv("SHEET_CLIENT_ID"),
        "auth_uri": os.getenv("SHEET_AUTH_URI"),
        "token_uri": os.getenv("SHEET_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("SHEET_AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.getenv("SHEET_CLIENT_X509_CERT_URL")
    }
    if not variables_keys['type']: # This is a check to see if it's on Heroku or not
        variables_keys = {
            "type": os.environ.get("SHEET_TYPE", None),
            "project_id": os.environ.get("SHEET_PROJECT_ID", None),
            "private_key_id": os.environ.get("SHEET_PRIVATE_KEY_ID", None),
            "private_key": os.environ.get("SHEET_PRIVATE_KEY", None),
            "client_email": os.environ.get("SHEET_CLIENT_EMAIL", None),
            "client_id": os.environ.get("SHEET_CLIENT_ID", None),
            "auth_uri": os.environ.get("SHEET_AUTH_URI", None),
            "token_uri": os.environ.get("SHEET_TOKEN_URI", None),
            "auth_provider_x509_cert_url": os.environ.get("SHEET_AUTH_PROVIDER_X509_CERT_URL", None),
            "client_x509_cert_url": os.environ.get("SHEET_CLIENT_X509_CERT_URL", None)
        }
    return variables_keys

    
def get_name_by_telegram_user(telegram_username, client):
    user_mapping_worksheet =  client.open_by_key(get_key_for_spreadsheet()).worksheet("Telegram Mapping")
    filtered_name_dict = filter(lambda user_json : (user_json['username'] == telegram_username), user_mapping_worksheet.get_all_records())
    return next(filtered_name_dict)['name']

def record_to_message_format(json_record):
    return "<code>" + json_record['Type'].split(" ")[0] + " " + json_record['Title'] + "</code>" + "\n"

def get_key_for_spreadsheet():
    key = os.getenv('SPREADSHEET_KEY')
    if not key:
        key=os.environ.get('SPREADSHEET_KEY', None)
    return key

def handle(update, context):
    relevant_shows_to_user = get_unseen_by_user(update.message.from_user['username'])
    context.bot.send_message(chat_id=update.effective_chat.id, text=relevant_shows_to_user, parse_mode=telegram.ParseMode.HTML)
