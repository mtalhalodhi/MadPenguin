import pandas
import random

#prints 'a owned b'
def own(a, b):
    return a + ' owned ' + b

def own_bot_command(update, context):
    a = update.message.from_user['username']
    b = ""
    if (len(context.args) > 0):
        b += " ".join(context.args)
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=own(a, b))