import os
import numpy as np
from werkzeug.utils import secure_filename
from flask import Flask, redirect, url_for, request, render_template
from keras.models import load_model
from keras.preprocessing import image


######################################################################################################

# Model saved with Keras model.save()
MODEL_PATH = 'Models/hotdog_classifier_final.h5'

print("model is loading.....")
model = load_model(MODEL_PATH)
print("model is loaded. Check http://127.0.0.1:5000/ ")


def predict(image_path, model):

    img = image.load_img(image_path, target_size=(229, 229))
    # (229,229) is the expected input size for InceptionV3
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img/255

    predict = model.predict_classes(img)

    if predict[0][0] == 0:
        result = 'Hotdog'
    else:
        result = 'Not Hotdog'

    return result
##################################################################################################


# Define a flask app
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', prediction=0)


@app.route('/predict', methods=['POST', 'GET'])
def upload():

    if request.method == 'POST':
        f = request.files["u_img"]

        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        r = predict(file_path, model)

        return r
    return None


if __name__ == '__main__':
    app.run(debug=True)
