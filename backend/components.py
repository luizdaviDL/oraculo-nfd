
import pandas as pd
import numpy as np
from PIL import Image
import re


import re

def is_valid_description_line(self, row):
    row = row.strip()

    if not row:
        return False

    row_upper = row.upper()

    # ❌ lixo conhecido
    lixo_keywords = [
        "DADOS ADICIONAIS",
        "INFORMAÇÕES COMPLEMENTARES",
        "INSCRIÇÃO",
        "VALOR TOTAL",
    ]

    if any(k in row_upper for k in lixo_keywords):
        return False

    # ✔ remove "Número do Pedido"
    row_clean = re.split(r"N[ÚU]MERO DO PEDIDO.*", row, flags=re.IGNORECASE)[0].strip()

    # ✔ remove padrões de caixa (CX 10, CX10)
    row_clean = re.sub(r"\bCX\s*\d+\b", "", row_clean, flags=re.IGNORECASE).strip()

    # ❌ se não sobrou nada → não é descrição
    if not row_clean:
        return False

    # ❌ se parece só número/valor
    if re.fullmatch(r"[\d\W]+", row_clean):
        return False

    return True


def find_ncm(value):
    index_ncm = None

    for i in range(1, len(value)):
        if re.match(r"^.", value[i]):
            number = re.sub(r"\D", "", value[i])

            if re.match(r"^\d{8}$", number):
                index_ncm = i
                break

    return index_ncm


def clear_null_lines(linhas):
    return [linha for linha in linhas if linha.strip()]


def refactor_values(value):
    value = value.strip()

    # limpar sujeira do OCR
    value = value.replace("|", " ")
    value = value.replace("“", " ")
    value = value.replace("!", " ")
    value = value.replace("_", " ")

    value = value.split('\n')

    return value


def is_line_trash(row):
    row_upper = row.upper()

    if "NÚMERO DO PEDIDO" in row_upper:
        # remove everything after "Número do Pedido"
        cleaned = re.split(r"N[ÚU]MERO DO PEDIDO.*", row_upper)[0].strip()

        # if nothing (or almost nothing) remains → it's trash
        if not cleaned or len(cleaned) < 3:
            return True

    return False


def clean_product_line(row):
    # remove tudo a partir de "Número do Pedido"
    cleaned = re.split(r"N[ÚU]MERO DO PEDIDO.*", row, flags=re.IGNORECASE)[0]

    return cleaned.strip()


import re

def is_valid_text(row):
    row = row.strip()

    if not row:
        return False

    # ❌ muita pontuação → lixo
    if len(re.findall(r"[^\w\s]", row)) > len(row) * 0.3:
        return False

    # remove números e símbolos
    letters_only = re.sub(r"[^A-Za-zÀ-ÿ ]", "", row)
    words = letters_only.split()

    if not words:
        return False

    # ❌ muitas palavras muito curtas
    validet_words = [p for p in words if len(p) > 2]

    if len(validet_words) / len(words) < 0.5:
        return False

    # ❌ padrão de letras aleatórias (tipo tTA, EXA, AA)
    letras = "".join(words)
    if re.search(r"(.)\1{2,}", letras):  # AAA, BBB etc
        return False

    return True



def is_end_of_products(row):
    row_upper = row.upper()

    # limpa OCR (remove lixo visual)
    row_clean = re.sub(r"[^A-Z\s]", " ", row_upper)

    # 🔥 palavras-chave que indicam fim da seção
    keywords = [
        ("MOV", "MER"),          # MOVIMENTAÇÃO DE MERCADORIA
        ("CALC", "ISS"),         # CALCULO DO ISS
        ("DADOS", "ADIC"),       # DADOS ADICIONAIS
        ("INFORM", "COMPL"),     # INFORMAÇÕES COMPLEMENTARES

    ]

    # verifica combinações
    for k1, k2 in keywords:
        if k1 in row_clean and k2 in row_clean:
            return True

    return False



def is_product_header(row):
    row = row.upper()

    # remove caracteres estranhos do OCR
    row_clean = re.sub(r"[^A-Z\s]", " ", row)

    palavras = row_clean.split()

    # aproximações (tolerância a erro OCR)
    has_dados = any(re.search(r"DAD", p) for p in palavras)
    has_produto = any(re.search(r"PROD", p) for p in palavras)
    has_servico = any(re.search(r"SERV", p) for p in palavras)

    # regra principal (genérica)
    if has_dados and has_produto:
        return True

    # fallback (algumas notas não têm "dados")
    if has_produto and has_servico:
        return True

    return False