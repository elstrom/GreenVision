from flask import Flask, render_template, request
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from io import BytesIO
import numpy as np

app = Flask(__name__)
model = tf.keras.models.load_model('model.h5', compile=False)
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='binary_crossentropy',
              metrics=[tf.keras.metrics.AUC(name='auc')])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['image']
    img = image.load_img(BytesIO(file.read()), target_size=(224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img/255.0

    prediction = model.predict(img)
    if prediction < 0.5:
        result = 'Organic Waste'
    else:
        result = 'Recycle Waste'

    return render_template('index.html', prediction_text='Prediction: {}'.format(result))


if __name__ == '__main__':
    app.run(debug=True)
