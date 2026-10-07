import time
from datetime import datetime

import requests

import banco

URL_INDICE = "https://developer.sankhya.com.br/llms.txt"


def baixar_texto(url):
    try:
        resposta = requests.get(
            url,
            timeout=20,
            headers={"User-Agent": "CP5-Python-Crawler"}
        )
        resposta.encoding = "utf-8"
        if resposta.status_code != 200:
            return ""
        return resposta.text
    except:
        return ""


def limitar(texto, tamanho):
    texto = texto.strip()
    while "  " in texto:
        texto = texto.replace("  ", " ")
    if len(texto) <= tamanho:
        return texto
    return texto[0:tamanho] + "..."


def descobrir_grupo(categoria):
    if categoria.startswith("Documentação API"):
        return "API"
    if categoria == "Recipes":
        return "Receita"
    if categoria == "Últimas Novidades":
        return "Novidade"
    return "Guia"


def descobrir_metodo(url):
    nome = url.split("/")[-1]
    nome = nome.lower()
    if nome.startswith("get"):
        return "GET"
    if nome.startswith("post"):
        return "POST"
    if nome.startswith("put"):
        return "PUT"
    if nome.startswith("delete"):
        return "DELETE"
    return "PAGINA"


def extrair_links(conteudo):
    linhas = conteudo.split("\n")
    categoria = "Sem categoria"
    paginas = []

    for linha in linhas:
        linha = linha.strip()

        if linha.startswith("## "):
            categoria = linha[3:].strip()
            continue

        if linha.startswith("- [") == False:
            continue

        inicio_titulo = linha.find("[")
        fim_titulo = linha.find("]")
        inicio_url = linha.find("](")
        fim_url = linha.find(")")

        if inicio_titulo == -1 or fim_titulo == -1 or inicio_url == -1 or fim_url == -1:
            continue

        titulo = linha[inicio_titulo + 1:fim_titulo].strip()
        url = linha[inicio_url + 2:fim_url].strip()
        resumo = ""

        if fim_url + 1 < len(linha):
            resto = linha[fim_url + 1:].strip()
            if resto.startswith(":"):
                resumo = resto[1:].strip()

        if titulo == "" or url == "":
            continue

        paginas.append({
            "titulo": titulo,
            "url": url,
            "categoria": categoria,
            "resumo": resumo
        })

    return paginas


def tirar_marcacao(texto):
    while "[" in texto and "](" in texto:
        inicio = texto.find("[")
        meio = texto.find("](", inicio)
        fim = texto.find(")", meio)
        if inicio == -1 or meio == -1 or fim == -1:
            break
        nome = texto[inicio + 1:meio]
        texto = texto[0:inicio] + nome + texto[fim + 1:]

    texto = texto.replace("**", "")
    texto = texto.replace("`", "")
    texto = texto.replace("\\", "")
    return texto.strip()


def linha_util(linha):
    if linha == "" or linha == "---":
        return False
    if linha[0] in "#<{*-|>!":
        return False
    if linha.startswith("updatedAt") or linha.startswith("agentTools"):
        return False
    return True


def pegar_trecho(texto):
    linhas = texto.split("\n")
    dentro_cabecalho = False
    ja_passou_cabecalho = False

    for linha in linhas:
        linha = linha.strip()

        if linha == "---" and ja_passou_cabecalho == False:
            if dentro_cabecalho == False:
                dentro_cabecalho = True
            else:
                dentro_cabecalho = False
                ja_passou_cabecalho = True
            continue

        if dentro_cabecalho:
            continue

        if linha_util(linha) == False:
            continue

        return limitar(tirar_marcacao(linha), 300)

    return ""


def coletar():
    print("Baixando o indice da documentacao Sankhya...", flush=True)
    indice = baixar_texto(URL_INDICE)
    if indice == "":
        print("Nao foi possivel baixar o indice.")
        return

    encontradas = extrair_links(indice)
    print("Paginas encontradas no indice:", len(encontradas), flush=True)

    novas = 0
    repetidas = 0
    data_coleta = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    for item in encontradas:
        if banco.buscar_por_url(item["url"]) is not None:
            repetidas = repetidas + 1
            continue

        texto_pagina = baixar_texto(item["url"])
        resumo = tirar_marcacao(item["resumo"])
        if resumo == "":
            resumo = pegar_trecho(texto_pagina)
        resumo = limitar(resumo, 350)

        pagina = {
            "id": banco.proximo_id(),
            "titulo": item["titulo"],
            "url": item["url"],
            "categoria": item["categoria"],
            "grupo": descobrir_grupo(item["categoria"]),
            "metodo": descobrir_metodo(item["url"]),
            "resumo": resumo,
            "data_coleta": data_coleta,
            "origem": URL_INDICE
        }

        banco.salvar_pagina(pagina)
        novas = novas + 1
        print("Salvou id", pagina["id"], flush=True)
        time.sleep(0.15)

    print("Coleta finalizada.")
    print("Novas:", novas)
    print("Ja existiam:", repetidas)


if __name__ == "__main__":
    coletar()
