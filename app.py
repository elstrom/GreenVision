import sys
sys.path.append('C:\\Users\\danra\\Downloads\\latihan\\GreenVision')

from flask import Flask, jsonify, render_template, request
from Bot.Run import get_bot_response
from Bot.utils.Translate import translate_google
from Bot.Knowledge import prompt_list as Knowledge

app = Flask(__name__, static_url_path='/static')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    # Panggil fungsi get_bot_response dengan user_input sebagai parameter
    response = get_bot_response(user_input, Knowledge)
    # Terjemahkan respons jika diperlukan
    translated_response = translate_google(response, 'en', 'id')
    return jsonify(response=translated_response)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
