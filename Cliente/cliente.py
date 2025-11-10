import httpx
import sys

BASE_URL = "http://127.0.0.1:8000"

def print_separador(titulo):
    print(f"\n--- [TESTE] {titulo} ---\n")

def testar_cliente():
    try:        
        print_separador("GET /produtos (Lista Inicial)")
        r_lista_inicial = httpx.get(f"{BASE_URL}/produtos")
        print(f"Status: {r_lista_inicial.status_code}")
        print(f"Total de produtos iniciais: {len(r_lista_inicial.json())}")

        print_separador("POST /produtos (Cadastrar novo produto)")
        produto_novo = {"nome": "Cadeira de Escritório", "categoria": "Móveis", "preco": 899.90}
        r_post = httpx.post(f"{BASE_URL}/produtos", json=produto_novo)
        print(f"Status: {r_post.status_code}")
        print(r_post.json())
        novo_id = r_post.json()['id']

        print_separador("GET /produtos/{id} (Buscar produto cadastrado)")
        r_get_id = httpx.get(f"{BASE_URL}/produtos/{novo_id}")
        print(f"Status: {r_get_id.status_code}")
        print(r_get_id.json())

        print_separador("PUT /produtos/{id} (Atualizar produto)")
        produto_atualizado = {"nome": "Cadeira de Escritório Ergonômica", "categoria": "Móveis Premium", "preco": 1050.0}
        r_put = httpx.put(f"{BASE_URL}/produtos/{novo_id}", json=produto_atualizado)
        print(f"Status: {r_put.status_code}")
        print(r_put.json())

        print_separador("GET /produtos/{id} (Verificar atualização)")
        r_get_id_atualizado = httpx.get(f"{BASE_URL}/produtos/{novo_id}")
        print(f"Status: {r_get_id_atualizado.status_code}")
        print(r_get_id_atualizado.json())

        print_separador("DELETE /produtos/{id} (Remover produto)")
        r_delete = httpx.delete(f"{BASE_URL}/produtos/{novo_id}")
        print(f"Status: {r_delete.status_code}")
        print(r_delete.json())

        print_separador("GET /produtos/{id} (Verificar remoção - Deve falhar 404)")
        r_get_id_removido = httpx.get(f"{BASE_URL}/produtos/{novo_id}")
        print(f"Status: {r_get_id_removido.status_code}")
        print(r_get_id_removido.json())
                
        print_separador("GET /produtos/stats/media-precos")
        r_media = httpx.get(f"{BASE_URL}/produtos/stats/media-precos")
        print(f"Status: {r_media.status_code}")
        print(r_media.json())

        print_separador("GET /produtos/stats/maior-preco")
        r_maior = httpx.get(f"{BASE_URL}/produtos/stats/maior-preco")
        print(f"Status: {r_maior.status_code}")
        print(r_maior.json())

        print_separador("GET /produtos/stats/menor-preco")
        r_menor = httpx.get(f"{BASE_URL}/produtos/stats/menor-preco")
        print(f"Status: {r_menor.status_code}")
        print(r_menor.json())

        print_separador("GET /produtos/stats/acima-media")
        r_acima = httpx.get(f"{BASE_URL}/produtos/stats/acima-media")
        print(f"Status: {r_acima.status_code}")
        print(f"Total de produtos acima da média: {len(r_acima.json())}")

        print_separador("GET /produtos/stats/abaixo-media")
        r_abaixo = httpx.get(f"{BASE_URL}/produtos/stats/abaixo-media")
        print(f"Status: {r_abaixo.status_code}")
        print(f"Total de produtos abaixo da média: {len(r_abaixo.json())}")

    except httpx.ConnectError:
        print(f"\n[ERRO] Não foi possível conectar ao servidor em {BASE_URL}")
        print("Verifique se o 'main.py' está rodando.")
        print("Use: uvicorn main:app --reload")
    except Exception as e:
        print(f"\n[ERRO INESPERADO] {e}")

if __name__ == "__main__":

    testar_cliente()
