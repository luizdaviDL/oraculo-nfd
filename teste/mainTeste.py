import fitz
from PIL import Image
import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

data = 'data.pdf'
doc = fitz.open(data)
doc = doc.load_page(0)
    
zoomResolution = fitz.Matrix(8,8)                 

image = doc.get_pixmap(matrix=zoomResolution)
image_object = Image.frombytes("RGB", [image.width, image.height], image.samples)
color = cv2.cvtColor(np.array(image_object), cv2.COLOR_RGB2BGR)
gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(
                    gray,
                    0,
                    255,
                    cv2.THRESH_BINARY + cv2.THRESH_OTSU
                )[1]
texto = pytesseract.image_to_string(thresh, lang="por")
cv2.imwrite("thresh.png", thresh)
final_text = texto.split("\n")




#texto_total += texto + "\n"




'''
ima= 'camelo.jpg'
with Image.open(ima) as im:
    ro = im.rotate(45)
    ro.save("camelo_rotacionado.jpg")
'''


