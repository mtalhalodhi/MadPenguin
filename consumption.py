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
    filtered_records = list(filter(lambda record : (record[name_on_sheet] == value),shows_list_worksheet.get_all_records()))

    unseen_telegram_message = ""
    for filtered_json in filtered_records:
        unseen_telegram_message += record_to_message_format(filtered_json)
    return unseen_telegram_message

def update_user_entry_to_new_value(telegram_username, entry_name, new_value):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(generate_google_creds_dict(), scope)
    client = gspread.authorize(creds)
    name_on_sheet = get_name_by_telegram_user(telegram_username, client)

    shows_list_worksheet = client.open_by_key(get_key_for_spreadsheet()).worksheet("Consumption Queue")
    cell_with_entry_name = shows_list_worksheet.find(entry_name)
    user_col = shows_list_worksheet.find(name_on_sheet).col

    if cell_with_entry_name:
        shows_list_worksheet.update_cell(cell_with_entry_name.row, user_col, new_value)

    return cell_with_entry_name

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
    return "<code>" + json_record['Type'].split(" ")[0] + " " + json_record['Title'] + "</code>" + "\n"

def get_key_for_spreadsheet():
    key = os.getenv('SPREADSHEET_KEY')
    if not key:
        key=os.environ.get('SPREADSHEET_KEY', None)
    return key

def handle_unseen(update, context):
    relevant_shows_to_user = get_value_by_user(update.message.from_user['username'], "No")
    context.bot.send_message(chat_id=update.effective_chat.id, text=relevant_shows_to_user, parse_mode=telegram.ParseMode.HTML)

def handle_seen(update, context):
    entry_name = ""
    if (len(context.args) > 0):
        entry_name += " ".join(context.args)
    telegram_user = update.message.from_user['username']
    if (update_user_entry_to_new_value(telegram_username=telegram_user, entry_name=entry_name, new_value="Yes")):
        context.bot.send_message(chat_id=update.effective_chat.id, text="I updated it, be grateful", parse_mode=telegram.ParseMode.HTML)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Wow you suck, I couldn't find: {}, prepare to be cussed!".format(entry_name), parse_mode=telegram.ParseMode.HTML)
        context.args = list(telegram_user)
        cuss.cuss(update, context)

def handle_not_interested(update, context):
    entry_name = ""
    if (len(context.args) > 0):
        entry_name += " ".join(context.args)
    telegram_user = update.message.from_user['username']
    if (update_user_entry_to_new_value(telegram_username=telegram_user, entry_name=entry_name, new_value="Not Interested")):
        context.bot.send_message(chat_id=update.effective_chat.id, text="I updated it, be grateful", parse_mode=telegram.ParseMode.HTML)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Wow you suck, I couldn't find: {}, prepare to be cussed!".format(entry_name), parse_mode=telegram.ParseMode.HTML)
        context.args = list(telegram_user)
        cuss.cuss(update, context)


def handle_in_progress(update, context):
    entry_name = ""
    if (len(context.args) > 0):
        entry_name += " ".join(context.args)
    telegram_user = update.message.from_user['username']
    if (update_user_entry_to_new_value(telegram_username=telegram_user, entry_name=entry_name, new_value="In Progress")):
        context.bot.send_message(chat_id=update.effective_chat.id, text="I updated it, be grateful", parse_mode=telegram.ParseMode.HTML)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Wow you suck, I couldn't find: {}, prepare to be cussed!".format(entry_name), parse_mode=telegram.ParseMode.HTML)
        context.args = list(telegram_user)
        cuss.cuss(update, context)

def add_content_to_spreadsheet(content_title, content_type, telegram_username, status):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(generate_google_creds_dict(), scope)
    client = gspread.authorize(creds)
    name_on_sheet = get_name_by_telegram_user(telegram_username, client)
    suitable_content_types = ["📽️ Movie", "📺 Series", "🇯🇵 Anime", "📚 Novel", "🎮 Game", "📃 Manga"]
    if (content_type not in suitable_content_types):
        return

    shows_list_worksheet = client.open_by_key(get_key_for_spreadsheet()).worksheet("Consumption Queue")
    shows_list_worksheet.append_row([content_title, content_type, name_on_sheet, status, status, "No", "No", "No", "No"])


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
