from flask import Flask, jsonify, render_template, request
from ..Run import get_bot_response, translate_text, Knowledge

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    # Panggil fungsi get_bot_response dengan user_input sebagai parameter
    response = get_bot_response(user_input, Knowledge)
    # Terjemahkan respons jika diperlukan
    translated_response = translate_text(response)
    return jsonify(response=translated_response)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
