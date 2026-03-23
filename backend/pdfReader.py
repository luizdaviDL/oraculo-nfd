from backend.image_manipulation import ImageManipulation
import re
from backend.components import refactor_values, clear_null_lines, find_ncm, is_line_trash,clean_product_line,is_valid_text,is_end_of_products,is_product_header


class PDFReader:

    def reade_imagem_pdf(self, value):
        
        text = ImageManipulation().get_text(value)
        allPages = text
        #linhas = linhas[62:]
        
        capturar = False

        produtos = []
        actual_product = None

        for page in allPages:
            page = page.strip()
                                    
            # limpar sujeira do OCR
            page = refactor_values(page)          
            page = clear_null_lines(page)
            
            for row in page:
                if is_end_of_products(row):
                    capturar = False
                    actual_product = None
                    break
                # detectar cabeçalho
                if is_product_header(row):
                    capturar = True
                    continue

                if capturar:

                    # detectar produto
                    #deve começar com 5 digitos ou mais no primeiro valor
                    if re.match(r"^\d{5,}", row):
                        partes = row.split()
                        codigo = partes[0]

                        indice_ncm = find_ncm(partes)
                       
                        if indice_ncm is None:
                            continue

                        if indice_ncm + 1 >= len(partes):
                            continue

                        descricao = " ".join(partes[1:indice_ncm])
                        quantidade = partes[indice_ncm + 1]

                        actual_product = {
                            "codigo": codigo,
                            "descricao": descricao,
                            "quantidade": quantidade
                        }

                        produtos.append(actual_product)

                    # 🔥 CONTINUAÇÃO DA DESCRIÇÃO                    
                    elif actual_product:
                        next_line = row.strip()

                        if not next_line:
                            continue

                        # ❌ se começar com número → provavelmente novo campo
                        if re.match(r"^\d", next_line):
                            actual_product = None
                            continue

                        # ❌ ignora lixo puro
                        if is_line_trash(next_line):
                            continue

                        # 🔥 limpa "Número do Pedido"
                        cleaned_line = clean_product_line(next_line)

                        # 🔥 remove padrão de caixa (CX 10, CX10)
                        cleaned_line = re.sub(r"\bCX\s*\d+\b", "", cleaned_line, flags=re.IGNORECASE).strip()

                        # ❌ se ficou vazio depois da limpeza → ignora
                        if not cleaned_line:
                            continue

                        # ❌ se não tem letra → não é descrição
                        if not re.search(r"[A-Za-z]", cleaned_line):
                            actual_product = None
                            continue
                        
                        if not is_valid_text(cleaned_line):
                            continue
                        # ✔ ainda é descrição → adiciona
                        actual_product["descricao"] += " " + cleaned_line

        return produtos