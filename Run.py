import openai
from typing import Union
from utils.Translate import *
from Knowledge import prompt_list

with open('hidden.txt') as file:
    openai.api_key = file.read()

def get_api_response(prompt: str) -> Union[str, None]:
    text: str | None = None

    try:
        response: dict = openai.Completion.create(
            model='gpt-3.5-turbo',
            prompt=prompt,
            temperature=0.6,
            max_tokens=110,
            top_p=1,
            best_of=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[' Human:', ' ID Answer:']
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
        pos: int = bot_response.find('\nID Answer: ')
        bot_response = bot_response[pos + 5:]
        bot_response = bot_response.replace('AI', 'GreenVision')
    else:
        bot_response = 'Something went wrong...'

    return bot_response

def translate_text(text):
    try:
        tts_en = translate_google(text, 'en', 'id')
        if tts_en:
            print(tts_en)
    except Exception as e:
        print("Error translating text: {0}".format(e))

def main():
    Knowledge = prompt_list

    while True:
        user_input: str = input('You: ')
        response: str = get_bot_response(user_input, Knowledge)
        translate_text(response)
        print(response)


if __name__ == '__main__':

    main()