import logging
from environs import Env
import vk_api
import random
from vk_api.longpoll import VkLongPoll, VkEventType


def echo(event, vk_bot):
    vk_bot.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1, 1000)
    )


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

    env = Env()
    env.read_env()

    vk_token = env.str('VK_API_KEY')
    vk_session = vk_api.VkApi(token=vk_token)
    vk_bot = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_bot)


if __name__ == '__main__':
    main()
