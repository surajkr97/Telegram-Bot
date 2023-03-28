from config import token

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import MessageEntity

endpoint_link = "http://127.0.0.1:5100/result/?query="

import urllib.request, json
def fetchjson(url):
    resp = urllib.request.urlopen(url)
    return json.loads(resp.read().decode())


def start(update, context):
    text="Hello {yourname}".format(yourname=update.effective_user.full_name)
    update.message.reply_text(text)

def download(update, context):
    x = update.message.parse_entities(types = MessageEntity.URL)
    msg = update.message.reply_text('Working on it...')
    for i in x:
        try:
            rjson = fetchjson(endpoint_link + x[i])
            title = rjson["song"]
            link = rjson["media_url"]
            msg.delete()
            update.message.reply_document(link, caption="Here is {}.".format(title))
            
        except:
            #raise
            continue
        if "error" in json:
            continue            
    msg.edit_text("I can't fetch from that url. Try Again.")

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.entity(MessageEntity.URL), download))

updater.start_polling()
updater.idle()