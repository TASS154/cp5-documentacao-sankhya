from pymongo import MongoClient

cliente = MongoClient("mongodb://localhost:27017/")
banco = cliente["documentacao_sankhya"]
colecao = banco["paginas"]


def limpar(pagina):
    if pagina is None:
        return None
    if "_id" in pagina:
        del pagina["_id"]
    return pagina


def buscar_por_url(url):
    return limpar(colecao.find_one({"url": url}))


def proximo_id():
    ultima = colecao.find_one(sort=[("id", -1)])
    if ultima is None:
        return 1
    return ultima["id"] + 1


def salvar_pagina(pagina):
    colecao.insert_one(pagina)


def listar_paginas():
    lista = []
    for pagina in colecao.find().sort("id", 1):
        lista.append(limpar(pagina))
    return lista


def buscar_pagina(pagina_id):
    return limpar(colecao.find_one({"id": pagina_id}))
