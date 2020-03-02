import os
import json
from logging import getLogger
import dialogflow_v2 as dialogflow


df_logger = getLogger('df_logger')


def get_dialogflow_answer(session_id, text):
    language_code = 'ru-RU'
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    session_client = dialogflow.SessionsClient()

    query_input = dialogflow.types.QueryInput(
        text=dialogflow.types.TextInput(text=text, language_code=language_code)
    )
    response = session_client.detect_intent(
        session=session_client.session_path(project_id, session_id), 
        query_input=query_input
    )
    df_logger.debug('Got response from DialogFlow')
    return response.query_result.fulfillment_text

def train_bot():
    with open('questions.json', 'r') as training_file:
        standard_queries = json.load(training_file)
    
    for intent_name, query_entity in standard_queries.items():
        training_phrases_parts = query_entity['questions']
        message_texts = [query_entity['answer']]
        create_intent(intent_name, training_phrases_parts, message_texts)

def create_intent(display_name, training_phrases_parts, message_texts):
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    intents_client = dialogflow.IntentsClient()
    parent = intents_client.project_agent_path(project_id)
    training_phrases = collect_training_phrases(training_phrases_parts)
    message = dialogflow.types.Intent.Message(
        text=dialogflow.types.Intent.Message.Text(text=message_texts)
    )

    intent = dialogflow.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message],
    )
    try:
        intents_client.create_intent(parent, intent)
        df_logger.debug(f'New intent "{display_name}" was created')
    except Exception:
        df_logger.exception('')

def collect_training_phrases(training_phrases_parts):
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.types.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    return training_phrases
