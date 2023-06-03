from flask import Flask, request
import numpy as np
from PIL import Image
from keras.models import Model
from keras.models import load_model
from flask_cors import CORS
import base64
import io

np.set_printoptions(suppress=True)
 
app = Flask(__name__)
cors = CORS(app, supports_credentials=True)

@app.route("/", methods=["GET", "POST"])
def judge():
    result = ""
    file = request.form['image']
    code = base64.b64decode(file.split(',')[1])
    img = Image.open(io.BytesIO(code))
    img = img.resize((150,150))

    img = np.array(img)/255
    img_expand = img[np.newaxis, ...]
    try:
        p = "サーバに画像がきたよ"
        
    except:
        result = "画像の形式が違うため，判定できません"
    print(p)
    
    return p

if __name__ == "__main__":
    app.run(debug=True)