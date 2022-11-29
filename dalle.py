import openai
import telegram

def get_image_url_from_prompt(prompt):
    openai.api_key='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'

    image_resp = openai.Image.create(prompt=prompt, n=4, size="512x512")

    return image_resp['data'][0]['url']

def generate_image_from_prompt(update, context):
    if (len(context.args) < 1):
        context.bot.send_message(chat_id=update.effective_chat.id, text="You need to provide a prompt to generate an image from", parse_mode=telegram.ParseMode.HTML)
        return
    image_prompt = " ".join(context.args[0:len(context.args)-1])
    image_url = get_image_url_from_prompt(image_prompt)

    context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url)

