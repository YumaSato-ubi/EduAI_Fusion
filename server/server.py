from flask import Flask, request
import numpy as np
from PIL import Image
from flask_cors import CORS
import base64
import io
import pyocr
from PIL import Image, ImageEnhance
import openai
import os
from gpt_scoring import gpt_scoring

tools = pyocr.get_available_tools()
tool = tools[0]
openai.api_key = "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"

np.set_printoptions(suppress=True)
 
app = Flask(__name__)
cors = CORS(app, supports_credentials=True)

@app.route("/", methods=["GET", "POST"])
def judge():
    result = ""
    file = request.form['image']
    code = base64.b64decode(file.split(',')[1])
    img = Image.open(io.BytesIO(code))
    img_g = img.convert('L') #Gray変換
    enhancer= ImageEnhance.Contrast(img_g) #コントラストを上げる
    img_con = enhancer.enhance(8.0) #コントラストを上げる

    try:
        # txt1 = tool.image_to_string(
        # img_con,
        # lang='jpn',
        # builder=pyocr.builders.TextBuilder(tesseract_layout=11))

        # response = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        # messages=[
        # {"role": "system", "content": "あなたは理科のテストを作成するプロです．"},
        # {"role": "user", "content": txt1 + " これは文字認識で読み込んだ理科のテストとその解答です．誤認識している部分を正確に修正し，このテストを丸つけしてください．なお，出力のフォーマットはつぎの通りにしてください．（例）(1):○\n(2):×..."}
        # ]   
        # )

        a = gpt_scoring()

        # print(response["choices"][0]["message"]["content"])
        
    except:
        result = "画像の形式が違うため，判定できません"
    
    return a

if __name__ == "__main__":
    app.run(debug=True)