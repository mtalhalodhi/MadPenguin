import pandas
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def random_curse():
    cusses_csv = pandas.read_csv('cusses.csv')

    iPrefix = random.randint(0, len(cusses_csv['prefix']) - 1)
    iMid = random.randint(0, len(cusses_csv['mid']) - 1)
    iEnd = random.randint(0, len(cusses_csv['end']) - 1)
    return cusses_csv['prefix'][iPrefix] + " " + cusses_csv['mid'][iMid] + " " + cusses_csv['end'][iEnd]

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
