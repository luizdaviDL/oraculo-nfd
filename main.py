from backend.pdfReader import PDFReader



if __name__ == "__main__":
    guia = 'guia.pdf'
    viagem = '5017772504'
    pdf = 'dfn Danone teste.pdf'
    
    textGet = PDFReader().reade_imagem_pdf(pdf)
    print(textGet)