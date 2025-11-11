import httpx
import sys

BASE_URL = "http://127.0.0.1:8000"

def print_separador(titulo):
    print(f"\n--- [TESTE] {titulo} ---\n")

def testar_cliente():
    try:
        #TESTANDO CRUD
        
        print_separador("GET /filmes (Lista Inicial)")
        r_lista_inicial = httpx.get(f"{BASE_URL}/filmes")
        print(f"Status: {r_lista_inicial.status_code}")
        print(f"Total de filmes iniciais: {len(r_lista_inicial.json())}")

        #POST  

        print_separador("POST /filmes (Cadastrar 'O Exorcista')")
        filme_novo_1 = {"nome": "O Exorcista", "categoria": "Terror", "nota_imdb": 8.1}
        r_post_1 = httpx.post(f"{BASE_URL}/filmes", json=filme_novo_1)
        print(f"Status: {r_post_1.status_code}")
        print(r_post_1.json())
        novo_id_1 = r_post_1.json()['id']

        #GET

        print_separador(f"GET /filmes/{novo_id_1} (Buscar O Exorcista)")
        r_get_id = httpx.get(f"{BASE_URL}/filmes/{novo_id_1}")
        print(f"Status: {r_get_id.status_code}")
        print(r_get_id.json())

        #PUT

        print_separador(f"PUT /filmes/{novo_id_1} (Atualizar O Exorcista)")
        filme_atualizado = {"nome": "O Exorcista (Versão do Diretor)", "categoria": "Terror", "nota_imdb": 8.2}
        r_put = httpx.put(f"{BASE_URL}/filmes/{novo_id_1}", json=filme_atualizado)
        print(f"Status: {r_put.status_code}")
        print(r_put.json())

        #BUSCA ATUALIZADA

        print_separador(f"GET /filmes/{novo_id_1} (Verificar atualização do Filme)")
        r_get_id_atualizado = httpx.get(f"{BASE_URL}/filmes/{novo_id_1}")
        print(f"Status: {r_get_id_atualizado.status_code}")
        print(r_get_id_atualizado.json())

        #DELETE

        print_separador(f"DELETE /filmes/{novo_id_1} (Remover Filme)")
        r_delete = httpx.delete(f"{BASE_URL}/filmes/{novo_id_1}")
        print(f"Status: {r_delete.status_code}")
        print(r_delete.json())

        #VERIFICA REMOCAO

        print_separador(f"GET /filmes/{novo_id_1} (Verificar remoção - Deve falhar 404)")
        r_get_id_removido = httpx.get(f"{BASE_URL}/filmes/{novo_id_1}")
        print(f"Status: {r_get_id_removido.status_code}")
        print(r_get_id_removido.json())
        
        #ESTATÍSTICAS 
        
        print_separador("GET /filmes/stats/media-notas")
        r_media = httpx.get(f"{BASE_URL}/filmes/stats/media-notas")
        print(f"Status: {r_media.status_code}")
        print(r_media.json())

        print_separador("GET /filmes/stats/maior-nota")
        r_maior = httpx.get(f"{BASE_URL}/filmes/stats/maior-nota")
        print(f"Status: {r_maior.status_code}")        
        dados_maior = r_maior.json()
        print(f"Filme de maior nota: {dados_maior['nome']} (Nota: {dados_maior['nota_imdb']})")

        print_separador("GET /filmes/stats/menor-nota")
        r_menor = httpx.get(f"{BASE_URL}/filmes/stats/menor-nota")
        print(f"Status: {r_menor.status_code}")
        dados_menor = r_menor.json()
        print(f"Filme de menor nota: {dados_menor['nome']} (Nota: {dados_menor['nota_imdb']})")

        print_separador("GET /filmes/stats/acima-media")
        r_acima = httpx.get(f"{BASE_URL}/filmes/stats/acima-media")
        print(f"Status: {r_acima.status_code}")
        print(f"Total de filmes acima da média: {len(r_acima.json())}")

        print_separador("GET /filmes/stats/abaixo-media")
        r_abaixo = httpx.get(f"{BASE_URL}/filmes/stats/abaixo-media")
        print(f"Status: {r_abaixo.status_code}")
        print(f"Total de filmes abaixo da média: {len(r_abaixo.json())}")

    except httpx.ConnectError:
        print(f"\n[ERRO] Não foi possível conectar ao servidor em {BASE_URL}")
        print("Verifique se o 'main.py' está rodando.")
    except Exception as e:
        print(f"\n[ERRO INESPERADO] {e}")

if __name__ == "__main__":
    testar_cliente()
