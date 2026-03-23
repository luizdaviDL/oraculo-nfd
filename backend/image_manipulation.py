import pandas as pd
import fitz
import pytesseract
import cv2
import numpy as np
from PIL import Image



class ImageManipulation:
    
    def get_text(self, pdf_path):
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        
        try:
            valieList = []
            doc = fitz.open(pdf_path)
            final_text = ""

            for page in doc:
                
                zoomResolution = fitz.Matrix(8, 8)  # aumentar o zoom da pagina do pdf                                
                #transformar essa pagina pdf em imagem em pixel (contem: altura, largura e os pixels da imagem)
                image = page.get_pixmap(matrix=zoomResolution)
        
                #transforma essa imagem que esta em pixel para um objeto de imagem, para assim podermos manipular a imagem
                #colocando cores, reduzindo o ruido, etc
                img = Image.frombytes("RGB", [image.width, image.height], image.samples)
                
                #troca a ordem das cores da imagem, de RGB para BGR, pois o OpenCV trabalha com a ordem BGR e o PIL trabalha com a ordem RGB
                img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

                #transforma a imagem que estava em bgr para cinza, para que o tesseract consiga identificar melhor o texto, pois o tesseract trabalha melhor com imagens em preto e branco
                gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
                #remover a cor do fundo da imagem, deixando o fundo branco e texto preto
                
                thresh = cv2.threshold(
                    gray,
                    0,
                    255,
                    cv2.THRESH_BINARY + cv2.THRESH_OTSU
                )[1]
                
        
                text = pytesseract.image_to_string(thresh, lang="por")

                final_text +=  text + "\n"
                valieList.append(text)
                
            return valieList

        except Exception as e:
            print(f"Erro ao processar PDF: {e}")
            return ""    