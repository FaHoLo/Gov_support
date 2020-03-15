import os
import log_config
import logging
import dialogflow_aps
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


tg_logger = logging.getLogger('tg_logger')


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
        handlers=[log_config.SendToTelegramHandler()]
    )
    load_dotenv()
    bot_token = os.getenv('TG_BOT_TOKEN')
    while True:
        try:
            start_tg_bot(bot_token)
        except Exception:
            tg_logger.exception('')
            continue

def start_tg_bot(bot_token):
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, send_dialogflow_answer_tg))
    tg_logger.debug('Bot starts polling')
    updater.start_polling()
    updater.idle()

def start(bot, update):
    update.message.reply_text('Здравствуйте!')

def send_dialogflow_answer_tg(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    query_result = dialogflow_aps.get_dialogflow_query_result(chat_id, text)
    update.message.reply_text(query_result.fulfillment_text)
    tg_logger.debug(f'Message has been sent to {update.message.from_user.username}')

if __name__ == '__main__':
    main()
    