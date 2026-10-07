import banco


def juntar(texto):
    return texto.lower().replace(" ", "")


def cabe_um_erro(a, b):
    if a == b:
        return True
    if abs(len(a) - len(b)) > 1:
        return False

    i = 0
    j = 0
    erros = 0

    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            i = i + 1
            j = j + 1
            continue

        erros = erros + 1
        if erros > 1:
            return False

        if len(a) == len(b):
            i = i + 1
            j = j + 1
        elif len(a) > len(b):
            i = i + 1
        else:
            j = j + 1

    if i < len(a) or j < len(b):
        erros = erros + 1

    return erros <= 1


def parece(texto, busca):
    texto = juntar(texto)
    busca = juntar(busca)

    if busca == "":
        return True
    if busca in texto:
        return True
    if len(busca) < 4:
        return False

    i = 0
    while i < len(texto):
        if cabe_um_erro(texto[i:i + len(busca)], busca):
            return True
        if cabe_um_erro(texto[i:i + len(busca) + 1], busca):
            return True
        if cabe_um_erro(texto[i:i + len(busca) - 1], busca):
            return True
        i = i + 1

    return False


def listar_paginas(busca, categoria):
    resultado = []

    for pagina in banco.listar_paginas():
        if categoria != "" and pagina["categoria"] != categoria:
            continue

        texto = pagina["titulo"] + pagina["resumo"] + pagina["grupo"]
        if parece(texto, busca):
            resultado.append(pagina)

    return resultado


def buscar_pagina(pagina_id):
    return banco.buscar_pagina(pagina_id)


def contar(paginas, campo):
    contagem = {}

    for pagina in paginas:
        nome = pagina[campo]
        if nome not in contagem:
            contagem[nome] = 0
        contagem[nome] = contagem[nome] + 1

    lista = []
    for nome in contagem:
        lista.append({campo: nome, "quantidade": contagem[nome]})

    return lista


def estatisticas():
    paginas = banco.listar_paginas()
    por_grupo = contar(paginas, "grupo")
    total_api = 0
    total_guias = 0

    for item in por_grupo:
        if item["grupo"] == "API":
            total_api = item["quantidade"]
        if item["grupo"] == "Guia":
            total_guias = item["quantidade"]

    return {
        "total": len(paginas),
        "total_api": total_api,
        "total_guias": total_guias,
        "por_categoria": contar(paginas, "categoria"),
        "por_grupo": por_grupo
    }
