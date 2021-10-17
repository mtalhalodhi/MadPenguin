import pip

import os
import pandas
import dotenv
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import cuss

def main():
    dotenv.load_dotenv()
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        bot_token=os.environ.get('PENGUIN_TELEGRAM_KEY', None)
    updater = Updater(token=bot_token, use_context=True, request_kwargs={
        #'proxy_url': 'http://196.1.95.117:80/',
    })
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    scope = ['https://www.googleapis.com/auth/spreadsheets']
    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open('')
    
    def start(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="THE MAD PENGUIN IS ALIVE!!!")
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    cuss_handler = CommandHandler('cuss', cuss.cuss)
    dispatcher.add_handler(cuss_handler)

    updater.start_polling()
main()
