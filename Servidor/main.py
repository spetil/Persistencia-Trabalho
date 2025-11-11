
import pandas as pd
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import asyncio
import os
from fastapi.middleware.cors import CORSMiddleware # permitir a comunição com o cliente html 
# https://fastapi.tiangolo.com/tutorial/cors/#more-info
# uvicorn main:app --reload

CSV_FILE = "filmes.csv"
lock = asyncio.Lock()

def gerar_dados_iniciais():
    dados = [
        {'id': 1, 'nome': 'Evil Dead 2', 'categoria': 'Terror', 'nota_imdb': 7.7},
        {'id': 2, 'nome': 'Pânico', 'categoria': 'Terror', 'nota_imdb': 7.4},
        {'id': 3, 'nome': 'Creep', 'categoria': 'Terror', 'nota_imdb': 6.3},
        {'id': 4, 'nome': 'Todo Mundo em Pânico', 'categoria': 'Comédia', 'nota_imdb': 6.2},
        {'id': 5, 'nome': 'O Poderoso Chefão', 'categoria': 'Drama', 'nota_imdb': 9.2},
        {'id': 6, 'nome': 'Batman: O Cavaleiro das Trevas', 'categoria': 'Ação', 'nota_imdb': 9.0},
        {'id': 7, 'nome': 'A Lista de Schindler', 'categoria': 'Biografia', 'nota_imdb': 8.9},
        {'id': 8, 'nome': 'Pulp Fiction: Tempo de Violência', 'categoria': 'Crime', 'nota_imdb': 8.9},
        {'id': 9, 'nome': 'O Senhor dos Anéis: O Retorno do Rei', 'categoria': 'Fantasia', 'nota_imdb': 8.9},
        {'id': 10, 'nome': 'Forrest Gump: O Contador de Histórias', 'categoria': 'Comédia', 'nota_imdb': 8.8},
        {'id': 11, 'nome': 'A Origem', 'categoria': 'Ficção Científica', 'nota_imdb': 8.8},
        {'id': 12, 'nome': 'Matrix', 'categoria': 'Ficção Científica', 'nota_imdb': 8.7},
        {'id': 13, 'nome': 'Os Sete Samurais', 'categoria': 'Aventura', 'nota_imdb': 8.6},
        {'id': 14, 'nome': 'Cidade de Deus', 'categoria': 'Crime', 'nota_imdb': 8.6},
        {'id': 15, 'nome': 'O Silêncio dos Inocentes', 'categoria': 'Suspense', 'nota_imdb': 8.6},
        {'id': 16, 'nome': 'Star Wars: Episódio V - O Império Contra-Ataca', 'categoria': 'Ficção Científica', 'nota_imdb': 8.7},
        {'id': 17, 'nome': 'Interestelar', 'categoria': 'Ficção Científica', 'nota_imdb': 8.6},
        {'id': 18, 'nome': 'Parasita', 'categoria': 'Suspense', 'nota_imdb': 8.6},
        {'id': 19, 'nome': 'Clube da Luta', 'categoria': 'Drama', 'nota_imdb': 8.8},
        {'id': 20, 'nome': 'O Resgate do Soldado Ryan', 'categoria': 'Guerra', 'nota_imdb': 8.6},
        {'id': 21, 'nome': 'Gladiador', 'categoria': 'Ação', 'nota_imdb': 8.5},
        {'id': 22, 'nome': 'O Grande Truque', 'categoria': 'Mistério', 'nota_imdb': 8.5},
        {'id': 23, 'nome': 'A Viagem de Chihiro', 'categoria': 'Animação', 'nota_imdb': 8.6},
        {'id': 24, 'nome': 'O Rei Leão', 'categoria': 'Animação', 'nota_imdb': 8.5},
        {'id': 25, 'nome': 'De Volta para o Futuro', 'categoria': 'Aventura', 'nota_imdb': 8.5},
        {'id': 26, 'nome': 'Whiplash: Em Busca da Perfeição', 'categoria': 'Drama', 'nota_imdb': 8.5},
        {'id': 27, 'nome': 'O Iluminado', 'categoria': 'Terror', 'nota_imdb': 8.4},
        {'id': 28, 'nome': 'Psicose', 'categoria': 'Terror', 'nota_imdb': 8.5},
        {'id': 29, 'nome': 'Laranja Mecânica', 'categoria': 'Crime', 'nota_imdb': 8.3},
        {'id': 30, 'nome': 'Janela Indiscreta', 'categoria': 'Mistério', 'nota_imdb': 8.5},
        {'id': 31, 'nome': 'Coringa', 'categoria': 'Drama', 'nota_imdb': 8.4},
        {'id': 32, 'nome': 'Apocalypse Now', 'categoria': 'Guerra', 'nota_imdb': 8.4},
        {'id': 33, 'nome': 'Alien, o Oitavo Passageiro', 'categoria': 'Ficção Científica', 'nota_imdb': 8.4},
        {'id': 34, 'nome': 'Blade Runner: O Caçador de Androides', 'categoria': 'Ficção Científica', 'nota_imdb': 8.1},
        {'id': 35, 'nome': 'WALL·E', 'categoria': 'Animação', 'nota_imdb': 8.4},
        {'id': 36, 'nome': 'Duro de Matar', 'categoria': 'Ação', 'nota_imdb': 8.2},
        {'id': 37, 'nome': 'Mad Max: Estrada da Fúria', 'categoria': 'Ação', 'nota_imdb': 8.1},
        {'id': 38, 'nome': 'O Exterminador do Futuro 2: O Julgamento Final', 'categoria': 'Ação', 'nota_imdb': 8.5},
        {'id': 39, 'nome': 'Indiana Jones e os Caçadores da Arca Perdida', 'categoria': 'Aventura', 'nota_imdb': 8.4},
        {'id': 40, 'nome': 'Brilho Eterno de uma Mente sem Lembranças', 'categoria': 'Romance', 'nota_imdb': 8.3},
        {'id': 41, 'nome': 'Se7en: Os Sete Crimes Capitais', 'categoria': 'Crime', 'nota_imdb': 8.6},
        {'id': 42, 'nome': 'Os Suspeitos', 'categoria': 'Mistério', 'nota_imdb': 8.5},
        {'id': 43, 'nome': 'Amnésia', 'categoria': 'Mistério', 'nota_imdb': 8.4},
        {'id': 44, 'nome': 'Réquiem para um Sonho', 'categoria': 'Drama', 'nota_imdb': 8.3},
        {'id': 45, 'nome': 'A Outra História Americana', 'categoria': 'Drama', 'nota_imdb': 8.5},
        {'id': 46, 'nome': 'Toy Story', 'categoria': 'Animação', 'nota_imdb': 8.3},
        {'id': 47, 'nome': 'Up: Altas Aventuras', 'categoria': 'Animação', 'nota_imdb': 8.2},
        {'id': 48, 'nome': 'O Labirinto do Fauno', 'categoria': 'Fantasia', 'nota_imdb': 8.2},
        {'id': 49, 'nome': 'O Grande Hotel Budapeste', 'categoria': 'Comédia', 'nota_imdb': 8.1},
        {'id': 50, 'nome': 'Monty Python e o Cálice Sagrado', 'categoria': 'Comédia', 'nota_imdb': 8.2},
    ]
    return pd.DataFrame(dados, columns=["id", "nome", "categoria", "nota_imdb"])

def salvar_dados(df: pd.DataFrame):
    df_para_salvar = df.copy()
    df_para_salvar['id'] = df_para_salvar['id'].astype(int)
    df_para_salvar.to_csv(CSV_FILE, index=False)

def carregar_dados():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            if df.empty:
                df = gerar_dados_iniciais()
                salvar_dados(df)
            else:
                df['id'] = df['id'].astype(int)
            return df
        except pd.errors.EmptyDataError:
            df = gerar_dados_iniciais()
            salvar_dados(df)
            return df
    else:
        df = gerar_dados_iniciais()
        salvar_dados(df)
        return df

db = carregar_dados()
proximo_id = (int(db['id'].max()) + 1) if not db.empty else 1

class FilmeBase(BaseModel):
    nome: str
    categoria: str
    nota_imdb: float

class Filme(FilmeBase):
    id: int

app = FastAPI(
    title="Trabalho 1/ API de Filmes",
    description="Lucas Cavalcante & Mateus Lima"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/filmes", response_model=Filme, status_code=status.HTTP_201_CREATED)
async def cadastrar_filme(filme: FilmeBase):
    global proximo_id, db
    async with lock:
        novo_filme = filme.model_dump()
        novo_filme['id'] = proximo_id        
        novo_filme_df = pd.DataFrame([novo_filme])
        db = pd.concat([db, novo_filme_df], ignore_index=True)
        
        salvar_dados(db)         
        proximo_id += 1
        return novo_filme

@app.get("/filmes", response_model=list[Filme])
def retornar_todos_filmes():
    return db.to_dict('records')

@app.get("/filmes/{id}", response_model=Filme)
def retornar_filme_por_id(id: int):
    filme = db[db['id'].astype(int) == id]
    if filme.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Filme com id {id} não encontrado"
        )
    return filme.to_dict('records')[0]

@app.put("/filmes/{id}", response_model=Filme)
async def atualizar_filme(id: int, filme_atualizado: FilmeBase):
    global db
    async with lock:
        indice = db.index[db['id'].astype(int) == id].tolist()
        if not indice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Filme com id {id} não encontrado"
            )
        idx = indice[0]
        db.loc[idx, 'nome'] = filme_atualizado.nome
        db.loc[idx, 'categoria'] = filme_atualizado.categoria
        db.loc[idx, 'nota_imdb'] = filme_atualizado.nota_imdb 
        
        salvar_dados(db) 
        filme_atualizado_completo = db.loc[idx].to_dict()
        return filme_atualizado_completo

@app.delete("/filmes/{id}")
async def remover_filme(id: int):
    global db
    async with lock:
        indice = db.index[db['id'].astype(int) == id].tolist()
        if not indice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Filme com id {id} não encontrado"
            )
        idx = indice[0]
        db = db.drop(idx).reset_index(drop=True)
        salvar_dados(db) 
        
        return {"message": "Filme removido com sucesso"}

@app.get("/filmes/stats/media-notas")
def obter_media_notas():
    if db.empty:
        return {"media_notas": 0}
    media = db['nota_imdb'].mean()
    return {"media_notas": round(media, 2)}

@app.get("/filmes/stats/maior-nota", response_model=list[Filme])
def obter_filme_maior_nota():
    if db.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Nenhum filme cadastrado"
        )
    maior_nota = db['nota_imdb'].max()
    filme = db[db['nota_imdb'] == maior_nota]
    return filme.to_dict('records')

@app.get("/filmes/stats/menor-nota", response_model=list[Filme])
def obter_filme_menor_nota():
    if db.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Nenhum filme cadastrado"
        )
    menor_nota = db['nota_imdb'].min()
    filme = db[db['nota_imdb'] == menor_nota]
    return filme.to_dict('records')

@app.get("/filmes/stats/acima-media", response_model=list[Filme])
def obter_filmes_acima_media():
    if db.empty:
        return []
    media = db['nota_imdb'].mean()
    filmes_acima_media = db[db['nota_imdb'] >= media]
    return filmes_acima_media.to_dict('records')

@app.get("/filmes/stats/abaixo-media", response_model=list[Filme])
def obter_filmes_abaixo_media():
    if db.empty:
        return []
    media = db['nota_imdb'].mean()
    filmes_abaixo_media = db[db['nota_imdb'] < media]
    
    return filmes_abaixo_media.to_dict('records')
