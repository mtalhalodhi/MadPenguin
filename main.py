import os
import pip
import pandas
import random
import dotenv
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

pip.main(['install', 'pandas'])
pip.main(['install', 'python-dotenv'])
pip.main(['install', 'python-telegram-bot'])

dotenv.load_dotenv()

updater = Updater(token=os.getenv('BOT_TOKEN'), use_context=True, request_kwargs={
    #'proxy_url': 'http://196.1.95.117:80/',
})
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

cusses_csv = pandas.read_csv('cusses.csv')

def random_curse():
    iPrefix = random.randint(0, len(cusses_csv['prefix']) - 1)
    iMid = random.randint(0, len(cusses_csv['mid']) - 1)
    iEnd = random.randint(0, len(cusses_csv['end']) - 1)
    return cusses_csv['prefix'][iPrefix] + " " + cusses_csv['mid'][iMid] + " " + cusses_csv['end'][iEnd]

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="THE MAD PENGUIN IS ALIVE!!!")
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def cuss(update, context):
    message = ""
    if (len(context.args) > 0):
        message += " ".join(context.args) + "! "
    curse = random_curse()
    start = curse.lower()[0]
    a_or_an = "a"
    if (start == "a" or start == "e" or start == "i" or start == "o" or start == "u"):
        a_or_an = "an"
    message += "Thou art " + a_or_an + " " + curse + "!!!"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
cuss_handler = CommandHandler('cuss', cuss)
dispatcher.add_handler(cuss_handler)

updater.start_polling()
