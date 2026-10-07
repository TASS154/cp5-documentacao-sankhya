# Documentacao Sankhya — CP5 Python

Sistema simples que coleta paginas publicas da documentacao Sankhya, grava no MongoDB, publica os dados em uma API FastAPI e mostra um dashboard.

O fluxo e:

Site -> Web Crawler -> MongoDB -> FastAPI -> Dashboard

## Site escolhido

Portal publico Sankhya Developer: https://developer.sankhya.com.br/

O crawler comeca pelo indice aberto da documentacao:

https://developer.sankhya.com.br/llms.txt

Esse indice lista guias, paginas de API, receitas e novidades. Nao sao coletados dados pessoais.

## Dados coletados

Cada pagina vira um documento com:

- `id`: numero inteiro
- `titulo`: nome da pagina
- `url`: endereco da pagina
- `categoria`: secao do indice, por exemplo `Guias: ADDON STUDIO`
- `grupo`: `Guia`, `API`, `Receita` ou `Novidade`
- `metodo`: `GET`, `POST`, `PUT`, `DELETE` ou `PAGINA`
- `resumo`: descricao curta encontrada no indice ou no texto da pagina
- `data_coleta`: data e hora da coleta
- `origem`: endereco do indice usado na coleta

Se a mesma `url` ja estiver no banco, o crawler nao grava de novo. Uma nova execucao nao apaga o que ja foi coletado.

## Banco de dados

MongoDB local, na porta padrao `27017`.

- Banco: `documentacao_sankhya`
- Colecao: `paginas`

Nao existe schema rigido. Todos os documentos seguem os campos acima.

## Como executar

O servico do MongoDB precisa estar ligado.

No CMD, dentro da pasta `projeto`:

```bat
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
python crawler.py
uvicorn main:app --reload
```

Depois abra:

- Dashboard: http://localhost:8000
- Documentacao da API: http://localhost:8000/docs

O crawler roda separado da API. Primeiro execute `python crawler.py`. So depois suba o `uvicorn`.

## Endpoints

### GET `/paginas`

Lista as paginas coletadas.

Filtros opcionais:

- `busca`: texto procurado no titulo, no resumo e no grupo. Os espacos sao ignorados. Com 4 letras ou mais, um erro de digitacao ainda encontra o texto.
- `categoria`: nome exato da categoria

Exemplo: `/paginas?busca=pedido de venda`

No dashboard a lista atualiza a cada letra digitada.

### GET `/paginas/{id}`

Retorna uma pagina pelo numero do `id`.

Se o id nao existir, a API responde `404`.

### GET `/estatisticas`

Retorna o total de registros, a quantidade de APIs, a quantidade de guias e as contagens por categoria e por grupo. O dashboard usa este endpoint.

## Dashboard

A pagina inicial consome somente a API. Ela mostra:

- o total de paginas
- a quantidade de paginas de API
- a quantidade de guias
- um grafico de barras por categoria
- um grafico de pizza por grupo
- uma pesquisa por texto e por categoria
- a tabela dos registros
- o resumo logo abaixo da linha clicada

## Organizacao do codigo

- `crawler.py`: coleta
- `banco.py`: gravacao e leitura no MongoDB
- `controller.py` e `main.py`: API
- `service.py`: filtros e estatisticas
- `static/index.html`: dashboard
