# para executar:
# uvicorn main:app --reload

from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import asyncio
import os

CSV_FILE = "produtos.csv"
lock = asyncio.Lock()

def gerar_dados_iniciais():
    dados = [
        {'id': 1, 'nome': 'Laptop Gamer', 'categoria': 'Eletrônicos', 'preco': 7500.0},
        {'id': 2, 'nome': 'Mouse Sem Fio', 'categoria': 'Acessórios', 'preco': 150.0},
        {'id': 3, 'nome': 'Teclado Mecânico', 'categoria': 'Acessórios', 'preco': 450.0},
        {'id': 4, 'nome': 'Monitor 4K', 'categoria': 'Monitores', 'preco': 2200.0},
        {'id': 5, 'nome': 'Cadeira Gamer', 'categoria': 'Móveis', 'preco': 1200.0},
        {'id': 6, 'nome': 'Headset 7.1', 'categoria': 'Acessórios', 'preco': 600.0},
        {'id': 7, 'nome': 'Smartphone', 'categoria': 'Eletrônicos', 'preco': 3500.0},
        {'id': 8, 'nome': 'Smartwatch', 'categoria': 'Eletrônicos', 'preco': 900.0},
        {'id': 9, 'nome': 'Webcam Full HD', 'categoria': 'Acessórios', 'preco': 300.0},
        {'id': 10, 'nome': 'Microfone Condensador', 'categoria': 'Acessórios', 'preco': 700.0},
        {'id': 11, 'nome': 'SSD 1TB', 'categoria': 'Componentes', 'preco': 800.0},
        {'id': 12, 'nome': 'Placa de Vídeo', 'categoria': 'Componentes', 'preco': 4500.0},
        {'id': 13, 'nome': 'Memória RAM 16GB', 'categoria': 'Componentes', 'preco': 500.0},
        {'id': 14, 'nome': 'Gabinete', 'categoria': 'Componentes', 'preco': 400.0},
        {'id': 15, 'nome': 'Cooler CPU', 'categoria': 'Componentes', 'preco': 250.0},
        {'id': 16, 'nome': 'Fonte 750W', 'categoria': 'Componentes', 'preco': 650.0},
        {'id': 17, 'nome': 'Mochila para Laptop', 'categoria': 'Acessórios', 'preco': 200.0},
        {'id': 18, 'nome': 'Filtro de Linha', 'categoria': 'Acessórios', 'preco': 80.0},
        {'id': 19, 'nome': 'Mousepad Grande', 'categoria': 'Acessórios', 'preco': 120.0},
        {'id': 20, 'nome': 'Lâmpada Inteligente', 'categoria': 'Casa', 'preco': 90.0},
        {'id': 21, 'nome': 'Aspirador Robô', 'categoria': 'Casa', 'preco': 1500.0},
        {'id': 22, 'nome': 'Cafeteira Elétrica', 'categoria': 'Casa', 'preco': 250.0},
        {'id': 23, 'nome': 'Liquidificador', 'categoria': 'Casa', 'preco': 180.0},
        {'id': 24, 'nome': 'Air Fryer', 'categoria': 'Casa', 'preco': 400.0},
        {'id': 25, 'nome': 'Notebook de Escritório', 'categoria': 'Eletrônicos', 'preco': 3200.0},
        {'id': 26, 'nome': 'Impressora Multifuncional', 'categoria': 'Eletrônicos', 'preco': 850.0},
        {'id': 27, 'nome': 'Roteador Mesh', 'categoria': 'Redes', 'preco': 700.0},
        {'id': 28, 'nome': 'Cabo de Rede 10m', 'categoria': 'Redes', 'preco': 50.0},
        {'id': 29, 'nome': 'HD Externo 2TB', 'categoria': 'Acessórios', 'preco': 450.0},
        {'id': 30, 'nome': 'Tablet', 'categoria': 'Eletrônicos', 'preco': 1700.0},
        {'id': 31, 'nome': 'Kindle', 'categoria': 'Eletrônicos', 'preco': 400.0}
    ]
    return pd.DataFrame(dados, columns=["id", "nome", "categoria", "preco"])

def carregar_dados():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            df['id'] = df['id'].astype(int)
            return df
        except pd.errors.EmptyDataError:
            return gerar_dados_iniciais()
    else:
        return gerar_dados_iniciais()

def salvar_dados(df: pd.DataFrame):
    df.to_csv(CSV_FILE, index=False)

db = carregar_dados()
proximo_id = (db['id'].max() + 1) if not db.empty else 1

class ProdutoBase(BaseModel):
    nome: str
    categoria: str
    preco: float

class Produto(ProdutoBase):
    id: int

app = FastAPI(
    title="API de Produtos (Trabalho 01)",
    description="Continuacao da Atividade 01 com persistencia em CSV e stats"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite TODAS as origens (ex: "file://", "http://localhost")
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

@app.post("/produtos", response_model=Produto, status_code=status.HTTP_201_CREATED)
async def cadastrar_produto(produto: ProdutoBase):
    global proximo_id, db
    async with lock:
        novo_produto = produto.model_dump()
        novo_produto['id'] = proximo_id
        db = db._append(novo_produto, ignore_index=True)
        salvar_dados(db)
        proximo_id += 1
        return novo_produto

@app.get("/produtos", response_model=list[Produto])
def retornar_todos_produtos():
    return db.to_dict('records')

@app.get("/produtos/{id}", response_model=Produto)
def retornar_produto_por_id(id: int):
    produto = db[db['id'] == id]
    if produto.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Produto com id {id} não encontrado"
        )
    return produto.to_dict('records')[0]

@app.put("/produtos/{id}", response_model=Produto)
async def atualizar_produto(id: int, produto_atualizado: ProdutoBase):
    global db
    async with lock:
        indice = db.index[db['id'] == id].tolist()
        if not indice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Produto com id {id} não encontrado"
            )
        idx = indice[0]
        db.loc[idx, 'nome'] = produto_atualizado.nome
        db.loc[idx, 'categoria'] = produto_atualizado.categoria
        db.loc[idx, 'preco'] = produto_atualizado.preco
        salvar_dados(db)
        produto_atualizado_completo = db.loc[idx].to_dict()
        return produto_atualizado_completo

@app.delete("/produtos/{id}")
async def remover_produto(id: int):
    global db
    async with lock:
        indice = db.index[db['id'] == id].tolist()
        if not indice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Produto com id {id} não encontrado"
            )
        idx = indice[0]
        db = db.drop(idx).reset_index(drop=True)
        salvar_dados(db)
        return {"message": "Produto removido com sucesso"}

@app.get("/produtos/stats/media-precos")
def obter_media_precos():
    if db.empty:
        return {"media": 0}
    media = db['preco'].mean()
    return {"media_precos": round(media, 2)}

@app.get("/produtos/stats/maior-preco", response_model=Produto)
def obter_produto_maior_preco():
    if db.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Nenhum produto cadastrado"
        )
    maior_preco = db['preco'].max()
    produto = db[db['preco'] == maior_preco]
    return produto.to_dict('records')[0]

@app.get("/produtos/stats/menor-preco", response_model=Produto)
def obter_produto_menor_preco():
    if db.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Nenhum produto cadastrado"
        )
    menor_preco = db['preco'].min()
    produto = db[db['preco'] == menor_preco]
    return produto.to_dict('records')[0]

@app.get("/produtos/stats/acima-media", response_model=list[Produto])
def obter_produtos_acima_media():
    if db.empty:
        return []
    media = db['preco'].mean()
    produtos_acima_media = db[db['preco'] >= media]
    return produtos_acima_media.to_dict('records')

@app.get("/produtos/stats/abaixo-media", response_model=list[Produto])
def obter_produtos_abaixo_media():
    if db.empty:
        return []
    media = db['preco'].mean()
    produtos_abaixo_media = db[db['preco'] < media]

    return produtos_abaixo_media.to_dict('records')
