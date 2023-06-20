from flask import Flask, render_template, request, jsonify
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from io import BytesIO
import numpy as np
from Bot.Run import get_bot_response
from Bot.utils.Translate import translate_google
from Bot.Knowledge import prompt_list as Knowledge
from flask import jsonify

app = Flask(__name__, static_url_path='/static')

model = tf.keras.models.load_model('model.h5', compile=False)
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='binary_crossentropy',
              metrics=[tf.keras.metrics.AUC(name='auc')])

# Buat generator gambar
image_generator = ImageDataGenerator(rescale=1./255)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['image']
    img = image.load_img(BytesIO(file.read()), target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)

    # Gunakan generator gambar untuk memuat batch gambar
    img_generator = image_generator.flow(img_array, shuffle=False)
    prediction = model.predict(img_generator)

    if prediction < 0.5:
        result = 'Organic Waste'
    else:
        result = 'Recycle Waste'

    return jsonify(response=result)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    response = get_bot_response(user_input, Knowledge)
    translated_response = translate_google(response, 'en', 'id')
    return jsonify(response=translated_response)

if __name__ == '__main__':
    app.run(debug=True)
