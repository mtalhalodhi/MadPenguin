import os

def getenv(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    
    envar = os.environ.get(text)

    context.bot.send_message(chat_id=chat_id, text=envar)