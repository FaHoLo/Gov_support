import os
import random
import log_config
import logging
import logging.config
import dialogflow_aps
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api


logging.config.dictConfig(log_config.LOGGER_CONFIG)
vk_logger = logging.getLogger('vk_logger')


def main():
    load_dotenv()
    while True:
        try:
            start_vk_bot()
        except Exception:
            vk_logger.exception('')
            continue

def start_vk_bot():
    vk_token = os.getenv('VK_GROUP_MESSAGE_TOKEN')
    vk_session = vk_api.VkApi(token=vk_token)
    vk_api_methods = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    vk_logger.debug('Bot starts polling')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            get_dialogflow_answer_vk(event, vk_api_methods)

def get_dialogflow_answer_vk(event, vk_api_methods):
    answer = dialogflow_aps.get_dialogflow_answer(event.user_id, event.text)
    if answer == 'Не совсем понимаю, о чём ты.':
        vk_logger.debug('Question was not recognized')
        return
    vk_api_methods.messages.send(
        user_id=event.user_id,
        message=answer,
        random_id=random.randint(1, 10000)
    )
    vk_logger.debug(f'Message has been sent to {event.user_id}')

if __name__ == '__main__':
    main()
    