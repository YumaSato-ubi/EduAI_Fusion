###################
# ライブラリインポート
####################
import pyocr
from PIL import Image, ImageEnhance
import os
import openai
import io
import os
import re
from google.cloud import vision
from google.oauth2 import service_account
import cv2
import json
import base64
import numpy as np


def gpt_scoring():
    ###################
    # 環境変数設定
    ####################
    #Path設定
    TESSERACT_PATH = '/usr/local/Cellar/tesseract/5.3.1/bin/tesseract' #インストールしたTesseract-OCRのpath
    TESSDATA_PATH = '/usr/local/Cellar/tesseract/5.3.1/share/tessdata' #tessdataのpath

    os.environ["PATH"] += os.pathsep + TESSERACT_PATH
    os.environ["TESSDATA_PREFIX"] = TESSDATA_PATH

    # 身元証明書のjson読み込み
    credentials = service_account.Credentials.from_service_account_file('/Users/satouyuuma/Downloads/composite-dream-388915-94b83c5c67e2.json')
    client = vision.ImageAnnotatorClient(credentials=credentials)

    ###############################
    # テスト画像→テキストデータへ変換
    ###############################
    # The name of the image file to annotate
    file_name = os.path.abspath('/Users/satouyuuma/Downloads/test_answer.jpg')

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)


    response = client.text_detection(image=image)
    texts = response.text_annotations

    #OCRエンジン取得
    tools = pyocr.get_available_tools()
    tool = tools[0]

    #OCRの設定 ※tesseract_layout=6が精度には重要。デフォルトは3
    builder = pyocr.builders.TextBuilder(tesseract_layout=3)

    #解析画像読み込み(雨ニモマケズ)
    test_img = Image.open('/Users/satouyuuma/Downloads/science_test.png') #他の拡張子でもOK
    #解析画像読み込み(雨ニモマケズ)
    answer_img = Image.open('/Users/satouyuuma/Downloads/test_answer.jpg') #他の拡張子でもOK

    #適当に画像処理(何もしないと結構制度悪いです・・)
    img_g = test_img.convert('L') #Gray変換
    enhancer= ImageEnhance.Contrast(img_g) #コントラストを上げる
    img_con = enhancer.enhance(2.0) #コントラストを上げる

    #適当に画像処理(何もしないと結構制度悪いです・・)
    answer_img_g = answer_img.convert('L') #Gray変換
    answer_enhancer= ImageEnhance.Contrast(answer_img_g) #コントラストを上げる
    answer_img_con = answer_enhancer.enhance(2.0) #コントラストを上げる

    #画像からOCRで日本語を読んで、文字列として取り出す
    test_txt_pyocr = tool.image_to_string(img_con , lang='jpn', builder=builder)
    answer_txt_pyocr = tool.image_to_string(answer_img_con , lang='jpn', builder=builder)

    #半角スペースを消す ※読みやすくするため
    txt_pyocr = test_txt_pyocr.replace(' ', '')
    answer_txt_pyocr = answer_txt_pyocr.replace(' ', '')
    # print(txt_pyocr)
    # print(answer_txt_pyocr)


    ####################################
    # テキストデータをchatGPTへ入力し採点
    ####################################
    openai.api_key = "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"

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "あなたは賢いAIです。"},
        {"role": "user", "content": "以下に示すのは、中学一年生の理科のテストです。\n"+  texts[0].description + "\n 以下が、上記のテストを解いた生徒の回答です。\n" + answer_txt_pyocr + "\n正解の場合は〇、間違っている場合はという下記の形式で答え合わせをお願いします。下記の形式のみ出力してください。説明などその他の出力は不要です。{\"(1)\": \"正解\", \"(2)\": \"間違い\"、\"(1)\": \"正解\} "}]
    )

    # print(response["choices"][0]["message"]["content"])

    answer_dic = json.loads(response["choices"][0]["message"]["content"])
    # print(type(answer_dic))
    # print(answer_dic)

    ##########################
    # 採点結果を画像データに反映
    ###########################
    #画像からOCRで日本語を読んで、文字列として取り出す
    #OCRの設定 ※tesseract_layout=6が精度には重要。デフォルトは3
    builder = pyocr.builders.WordBoxBuilder(tesseract_layout=3)

    #解析画像読み込み(雨ニモマケズ)
    img = Image.open('/Users/satouyuuma/Downloads/test_answer.jpg') #他の拡張子でもOK

    #適当に画像処理(何もしないと結構制度悪いです・・)
    img_g = img.convert('L') #Gray変換
    enhancer= ImageEnhance.Contrast(img_g) #コントラストを上げる
    img_con = enhancer.enhance(2.0) #コントラストを上げる

    #画像からOCRで日本語を読んで、文字列として取り出す
    txt_pyocr = tool.image_to_string(img_con , lang='jpn', builder=builder)

    img2 = cv2.imread('/Users/satouyuuma/Downloads/test_answer.jpg')

    for res in txt_pyocr:
        for key, value in answer_dic.items():
            if re.compile(key).search(res.content) and value=="正解":
                cv2.circle(img2, (int((res.position[1][0] - res.position[0][0])/2 + res.position[0][0]),int((res.position[1][1] - res.position[0][1])/2 + res.position[0][1])), 20, (0,0,255), thickness=1)
            if re.compile(key).search(res.content) and value=="間違い":
                cv2.line(img2, res.position[0], res.position[1], (0,0,255), thickness=1)
                cv2.line(img2, (res.position[1][0], res.position[0][1]), (res.position[0][0], res.position[1][1]), (0,0,255), thickness=1)      
    ret, dst_data = cv2.imencode('.jpg', img2)
    dst_str = base64.b64encode(dst_data)

    return dst_str
# gpt_scoring()
# gpt_scoring()