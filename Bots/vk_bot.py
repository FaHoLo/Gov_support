import os
import random
import log_config
import logging
import dialogflow_aps
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api


vk_logger = logging.getLogger('vk_logger')


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
        handlers=[log_config.SendToTelegramHandler()]
    )
    load_dotenv()
    vk_token = os.getenv('VK_GROUP_MESSAGE_TOKEN')
    while True:
        try:
            start_vk_bot(vk_token)
        except Exception:
            vk_logger.exception('')
            continue

def start_vk_bot(vk_token):
    vk_session = vk_api.VkApi(token=vk_token)
    vk_api_methods = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    vk_logger.debug('Bot starts polling')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_dialogflow_answer_vk(event, vk_api_methods)

def send_dialogflow_answer_vk(event, vk_api_methods):
    query_result = dialogflow_aps.get_dialogflow_query_result(event.user_id, event.text)
    if query_result.intent.is_fallback:
        vk_logger.debug('Question was not recognized')
        return
    vk_api_methods.messages.send(
        user_id=event.user_id,
        message=query_result.fulfillment_text,
        random_id=random.randint(1, 10000)
    )
    vk_logger.debug(f'Message has been sent to {event.user_id}')

if __name__ == '__main__':
    main()
    