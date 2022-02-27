import logging

import telegram
from environs import Env
from google.cloud import dialogflow
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from dialog_flow import detect_intent_texts
from tg_logs_handler import TgLogsHandler

logger = logging.getLogger(__name__)


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Обнаружена база повстанцев!")


def print_ai_answer(update, context):
    client_text = update.message.text
    session_id = update.effective_chat.id
    language_code = 'ru'
    project_id = context.bot_data['project_id']
    ai_answer = detect_intent_texts(project_id, session_id, client_text,
                                    language_code).fulfillment_text
    update.message.reply_text(ai_answer)


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.DEBUG)

    env = Env()
    env.read_env()

    project_id = env.str('DF_PROJECT_ID')
    bot_token = env.str('TG_BOT_TOKEN')
    admin_chat_id = env.str('ADMIN_BOT_CHAT_ID')
    bot = telegram.Bot(token=bot_token)
    try:
        updater = Updater(bot_token)
        dispatcher = updater.dispatcher
        bot_data = {
            "project_id": project_id,
        }
        logger.addHandler(TgLogsHandler(bot, admin_chat_id))
        logger.info('запущен tel_bot')

        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(MessageHandler(Filters.text, print_ai_answer))
        dispatcher.bot_data = bot_data

        updater.start_polling()
        updater.idle()
    except Exception as error:
        logging.exception(f"tel_bot упал с ошибкой: {error}")


if __name__ == '__main__':
    main()
