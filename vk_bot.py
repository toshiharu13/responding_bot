import logging
from environs import Env
import vk_api
import random
from vk_api.longpoll import VkLongPoll, VkEventType

from dialog_flow import detect_intent_texts


def get_ai_answer(event, vk_bot, project_id):
    client_text = event.text
    user_id = event.user_id
    ai_answer = detect_intent_texts(project_id, user_id, client_text,
                                    language_code='ru')
    #print(ai_answer)
    vk_bot.messages.send(
        user_id=event.user_id,
        message=ai_answer,
        random_id=random.randint(1, 1000)
    )


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

    env = Env()
    env.read_env()

    project_id = env.str('DF_PROJECT_ID')
    vk_token = env.str('VK_API_KEY')
    vk_session = vk_api.VkApi(token=vk_token)
    vk_bot = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            get_ai_answer(event, vk_bot, project_id)


if __name__ == '__main__':
    main()
