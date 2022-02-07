import os

def getenv(update, context):
    chat_id = update.message.chat_id
    message = ""
    if (len(context.args) > 0):
        message = context.args[0]
    
    envar = os.environ.get(message)

    context.bot.send_message(chat_id=chat_id, text=envar)