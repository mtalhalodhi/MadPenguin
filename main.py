import pip

import os
import pandas
import dotenv
import logging
from setuptools import Command
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from oauth2client.service_account import ServiceAccountCredentials

import cuss
import consumption
import own

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

    def start(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="THE MAD PENGUIN IS ALIVE!!!")
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    cuss_handler = CommandHandler('cuss', cuss.cuss)
    dispatcher.add_handler(cuss_handler)

    unseen_sheet_handler = CommandHandler('unseen', consumption.handle_unseen)
    dispatcher.add_handler(unseen_sheet_handler)

    own_handler = CommandHandler('own', own.own_bot_command)
    dispatcher.add_handler(own_handler)

    mark_seen_sheet_handler = CommandHandler('seen',  consumption.handle_seen)
    dispatcher.add_handler(mark_seen_sheet_handler)

    mark_not_interested_handler = CommandHandler('notinterested', consumption.handle_not_interested)
    dispatcher.add_handler(mark_not_interested_handler)

    mark_in_progress_handler = CommandHandler('inprogress', consumption.handle_in_progress)
    dispatcher.add_handler(mark_in_progress_handler)

    my_progress_handler = CommandHandler('myprogress', consumption.handle_my_progress)
    dispatcher.add_handler(my_progress_handler)

    updater.start_polling()
main()
