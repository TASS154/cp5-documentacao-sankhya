from fastapi import APIRouter, HTTPException

import service

router = APIRouter()


@router.get("/paginas")
def listar_paginas(busca: str = "", categoria: str = ""):
    return service.listar_paginas(busca, categoria)


@router.get("/paginas/{pagina_id}")
def buscar_pagina(pagina_id: int):
    pagina = service.buscar_pagina(pagina_id)
    if pagina is None:
        raise HTTPException(status_code=404, detail="Página não encontrada")
    return pagina


@router.get("/estatisticas")
def estatisticas():
    return service.estatisticas()
