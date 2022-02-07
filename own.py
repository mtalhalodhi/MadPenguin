import pandas
import random


def random_own():
    csv = pandas.read_csv('owns.csv')
    i = random.randint(0, len(csv['owns']) - 1)
    return csv["owns"][i]


def own(a, b):
    return random_own().replace("<a>", a).replace("<b>", b)


def own_bot_command(update, context):
    a = update.message.from_user['username']
    b = ""
    if (len(context.args) > 0):
        b += " ".join(context.args)

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=own("@" + a, b))
