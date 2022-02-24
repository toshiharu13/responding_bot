import logging
from environs import Env
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from google.cloud import dialogflow

from dialog_flow import detect_intent_texts


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Обнаружена база повстанцев!")


def get_answer(update, context):
    client_text = update.message.text
    session_id = update.effective_chat.id
    language_code = 'ru'
    project_id = context.bot_data['project_id']
    ai_answer = detect_intent_texts(project_id, session_id, client_text, language_code)
    update.message.reply_text(ai_answer)


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

    env = Env()
    env.read_env()

    project_id = env.str('DF_PROJECT_ID')
    bot_token = env.str('TG_BOT_TOKEN')
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher

    bot_data = {
        "project_id": project_id,
        #"sesion_id": session_id,
    }
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, get_answer))
    dispatcher.bot_data = bot_data

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
