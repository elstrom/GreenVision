import openai
from typing import Union
from Bot.utils.Translate import *
from Bot.Knowledge import prompt_list

with open('bot\hidden.txt') as file:
    openai.api_key = file.read()

def get_api_response(prompt: str) -> Union[str, None]:
    text: str | None = None

    try:
        response: dict = openai.Completion.create(
            model='text-curie-001',
            prompt=prompt,
            temperature=0.7,
            max_tokens=110,
            top_p=0.9,
            best_of=2,
            frequency_penalty=0.5,
            presence_penalty=0.5,
            stop=[' Human:', ' ID Answer:', '?']
        )

        choices: dict = response.get('choices')[0]
        text = choices.get('text')

    except Exception as e:
        print('ERROR:', e)

    return text


def update_list(message: str, pl: list[str]):
    pl.append(message)


def create_prompt(message: str, pl: list[str]) -> str:
    p_message: str = f'\nHuman: {message}'
    update_list(p_message, pl)
    prompt: str = ''.join(pl)
    return prompt


def get_bot_response(message: str, pl: list[str]) -> str:
    prompt: str = create_prompt(message, pl)
    bot_response: str = get_api_response(prompt)

    if bot_response:
        update_list(bot_response, pl)
        pos: int = bot_response.find('ID Answer: ')
        bot_response = bot_response[pos + 5:]

    else:
        bot_response = 'Something went wrong...'

    return bot_response

def translate_text(text):
    try:
        tts_id = translate_google(text, 'en', 'id')
        print("ID Answer: " + tts_id)
    except Exception as e:
        print("Error translating text: {0}".format(e))

def main():
    Knowledge = prompt_list

    while True:
        user_input: str = input('You: ')
        response: str = get_bot_response(user_input, Knowledge)
        translate_text(response)


if __name__ == '__main__':

    main()