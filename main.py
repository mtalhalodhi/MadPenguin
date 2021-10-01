import pip
pip.main(['install', 'pandas'])
pip.main(['install', 'python-dotenv'])
pip.main(['install', 'python-telegram-bot'])

import os
import pandas
import random
import dotenv
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import cuss

def main():
    dotenv.load_dotenv()
    updater = Updater(token=os.getenv('BOT_TOKEN'), use_context=True, request_kwargs={
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

    updater.start_polling()
main()
