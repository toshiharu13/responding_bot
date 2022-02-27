import logging
import random

import telegram
import vk_api
from environs import Env
from vk_api.longpoll import VkEventType, VkLongPoll

from dialog_flow import detect_intent_texts
from tg_logs_handler import TgLogsHandler

logger = logging.getLogger(__name__)


def print_ai_answer(event, vk_bot, project_id):
    client_text = event.text
    user_id = event.user_id
    ai_answer = detect_intent_texts(project_id, user_id, client_text,
                                    language_code='ru')
    if not ai_answer.intent.is_fallback:
        vk_bot.messages.send(
            user_id=event.user_id,
            message=ai_answer.fulfillment_text,
            random_id=random.randint(1, 1000))


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.DEBUG)

    env = Env()
    env.read_env()

    project_id = env.str('DF_PROJECT_ID')
    vk_token = env.str('VK_API_KEY')
    bot_token = env.str('TG_BOT_TOKEN')
    admin_chat_id = env.str('ADMIN_BOT_CHAT_ID')
    vk_session = vk_api.VkApi(token=vk_token)
    vk_bot = vk_session.get_api()

    bot = telegram.Bot(token=bot_token)

    logger.addHandler(TgLogsHandler(bot, admin_chat_id))
    logger.info('запущен vk_bot')
    try:
        longpoll = VkLongPoll(vk_session)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                print_ai_answer(event, vk_bot, project_id)
    except Exception as error:
        logger.exception(f"vk_bot упал с ошибкой: {error}")


if __name__ == '__main__':
    main()
