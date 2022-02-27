import json
import logging

from environs import Env


def create_intent(project_id, display_name, training_phrases_parts,
                  message_texts):
    """Создаёт список интентов из json файла"""
    from google.cloud import dialogflow

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)

        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message],)

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    logging.info('Intent created: {}'.format(response))


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

    env = Env()
    env.read_env()

    project_id = env.str('DF_PROJECT_ID')
    with open("new_intent.json", "r", encoding='utf-8') as my_file:
        file_contents = json.load(my_file)
        for key in file_contents:
            print('keysss: %s, valuess: %s' % (key, file_contents[key]))
            job_intent = file_contents[key]
            display_name = key
            training_phrases_parts = job_intent['questions']
            message_text = job_intent['answer']
            message_texts = [message_text]
            create_intent(project_id, display_name, training_phrases_parts,
                          message_texts)


if __name__ == '__main__':
    main()
