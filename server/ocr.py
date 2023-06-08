import pyocr
from PIL import Image, ImageEnhance
import os

tools = pyocr.get_available_tools()
tool = tools[0]

img = Image.open('アメニモマケズ.jpeg')
img_g = img.convert('L') #Gray変換
enhancer= ImageEnhance.Contrast(img_g) #コントラストを上げる
img_con = enhancer.enhance(2.0) #コントラストを上げる
txt1 = tool.image_to_string(
    img_con,
    lang='jpn',
    builder=pyocr.builders.TextBuilder(tesseract_layout=6)
)

print(txt1)