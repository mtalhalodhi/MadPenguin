import gspread
from oauth2client.service_account import ServiceAccountCredentials
import telegram
import os
import cuss

def get_value_by_user(telegram_username, value):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(generate_google_creds_dict(), scope)
    client = gspread.authorize(creds)
    name_on_sheet = get_name_by_telegram_user(telegram_username, client)

    shows_list_worksheet = client.open_by_key(get_key_for_spreadsheet()).worksheet("Consumption Queue")

    # Get all data with row number mapped to all values
    all_data = shows_list_worksheet.get_all_records()
    filtered_records = []
    for index, data in enumerate(all_data):
        if data[name_on_sheet] == value:
            filtered_records.append((index+1, data))

    unseen_telegram_message = ""
    for filtered_json in filtered_records:
        unseen_telegram_message += record_to_message_format(filtered_json)
    return unseen_telegram_message

def update_user_entry_to_new_value(telegram_username, new_value, entry_row_number):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(generate_google_creds_dict(), scope)
    client = gspread.authorize(creds)
    name_on_sheet = get_name_by_telegram_user(telegram_username, client)

    shows_list_worksheet = client.open_by_key(get_key_for_spreadsheet()).worksheet("Consumption Queue")
    user_col = shows_list_worksheet.find(name_on_sheet).col
    return shows_list_worksheet.update_cell(entry_row_number + 1, user_col, new_value)

def generate_google_creds_dict():
    variables_keys = {
        "type": os.getenv('SHEET_TYPE'),
        "project_id": os.getenv('SHEET_PROJECT_ID'),
        "private_key_id": os.getenv('SHEET_PRIVATE_KEY_ID'),
        "private_key": os.getenv('SHEET_PRIVATE_KEY'),
        "client_email": os.getenv('SHEET_CLIENT_EMAIL'),
        "client_id": os.getenv('SHEET_CLIENT_ID'),
        "auth_uri": os.getenv('SHEET_AUTH_URI'),
        "token_uri": os.getenv('SHEET_TOKEN_URI'),
        "auth_provider_x509_cert_url": os.getenv('SHEET_AUTH_PROVIDER_X509_CERT_URL'),
        "client_x509_cert_url": os.getenv('SHEET_CLIENT_X509_CERT_URL')
    }
    if not os.getenv("SHEET_TYPE"): # This is a check to see if it's on Heroku or not
        return {
            "type": os.environ.get('SHEET_TYPE', None),
            "project_id": os.environ.get('SHEET_PROJECT_ID', None),
            "private_key_id": os.environ.get('SHEET_PRIVATE_KEY_ID', None),
            "private_key": os.environ.get('SHEET_PRIVATE_KEY', None),
            "client_email": os.environ.get('SHEET_CLIENT_EMAIL', None),
            "client_id": os.environ.get('SHEET_CLIENT_ID', None),
            "auth_uri": os.environ.get('SHEET_AUTH_URI', None),
            "token_uri": os.environ.get('SHEET_TOKEN_URI', None),
            "auth_provider_x509_cert_url": os.environ.get('SHEET_AUTH_PROVIDER_X509_CERT_URL', None),
            "client_x509_cert_url": os.environ.get('SHEET_CLIENT_X509_CERT_URL', None)
        }
    return variables_keys

def get_name_by_telegram_user(telegram_username, client):
    user_mapping_worksheet =  client.open_by_key(get_key_for_spreadsheet()).worksheet("Telegram Mapping")
    filtered_name_dict = filter(lambda user_json : (user_json['username'] == telegram_username), user_mapping_worksheet.get_all_records())
    return next(filtered_name_dict)['name']

def record_to_message_format(json_record):
    return str(json_record[0]) + " <code>" + json_record[1]['Type'].split(" ")[0] + " " + json_record[1]['Title'] + "</code>" + "\n"

def get_key_for_spreadsheet():
    key = os.getenv('SPREADSHEET_KEY')
    if not key:
        key=os.environ.get('SPREADSHEET_KEY', None)
    return key

def handle_unseen(update, context):
    relevant_shows_to_user = get_value_by_user(update.message.from_user['username'], "No")
    context.bot.send_message(chat_id=update.effective_chat.id, text=relevant_shows_to_user, parse_mode=telegram.ParseMode.HTML)

def handle_seen(update, context):
    extract_cell_number_and_update(update, context, "Yes")

def handle_not_interested(update, context):
    extract_cell_number_and_update(update, context, "Not Interested")

def handle_in_progress(update, context):
    extract_cell_number_and_update(update, context, "In Progress")

def extract_cell_number_and_update(update, context, new_value):
    entry_row_string = ""
    entry_row_number= -1
    if (len(context.args) > 0):
        entry_row_string += "".join(context.args)
        entry_row_number = int(entry_row_string)
    telegram_user = update.message.from_user['username']
    if (update_user_entry_to_new_value(telegram_username=telegram_user, entry_row_number= entry_row_number, new_value=new_value)):
        context.bot.send_message(chat_id=update.effective_chat.id, text="I updated it, be grateful", parse_mode=telegram.ParseMode.HTML)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Wow you suck, I couldn't find anything for number: {}, prepare to be cussed!".format(entry_row_number), parse_mode=telegram.ParseMode.HTML)
        context.args = list(telegram_user)
        cuss.cuss(update, context)

def add_content_to_spreadsheet(content_title, content_type, telegram_username, status):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(generate_google_creds_dict(), scope)
    client = gspread.authorize(creds)
    name_on_sheet = get_name_by_telegram_user(telegram_username, client)
    suitable_content_types_without_icon = ["Movie", "Series", "Anime", "Novel", "Game", "Manga"]
    suitable_content_types = ["📽️ Movie", "📺 Series", "🇯🇵 Anime", "📚 Novel", "🎮 Game", "📃 Manga"]
    if (content_type not in suitable_content_types_without_icon):
        return
    content_type_with_icon = suitable_content_types[suitable_content_types_without_icon.index(content_type)]

    shows_list_worksheet = client.open_by_key(get_key_for_spreadsheet()).worksheet("Consumption Queue")
    shows_list_worksheet.append_row([content_title, content_type_with_icon, name_on_sheet, status, status, "No", "No", "No", "No"])


def handle_my_progress(update, context):
    relevant_shows_to_user = get_value_by_user(update.message.from_user['username'], "In Progress")
    context.bot.send_message(chat_id=update.effective_chat.id, text=relevant_shows_to_user, parse_mode=telegram.ParseMode.HTML)

def handle_add_content(update, context):
    if (len(context.args) < 2):
        context.bot.send_message(chat_id=update.effective_chat.id, text="You need to provide a title and a type", parse_mode=telegram.ParseMode.HTML)
        return
    content_title = " ".join(context.args[0:len(context.args)-1])
    content_type = context.args[len(context.args)-1]
    add_content_to_spreadsheet(content_title, content_type, update.message.from_user['username'], "In Progress")
    context.bot.send_message(chat_id=update.effective_chat.id, text="I added it to the queue", parse_mode=telegram.ParseMode.HTML)
