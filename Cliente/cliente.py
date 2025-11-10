import httpx
import sys

BASE_URL = "http://127.0.0.1:8000"

def print_separador(titulo):
    print(f"\n--- [TESTE] {titulo} ---\n")

def testar_cliente():
    try:
        #TESTANDO CRUD
        
        print_separador("GET /produtos (Lista Inicial)")
        r_lista_inicial = httpx.get(f"{BASE_URL}/produtos")
        print(f"Status: {r_lista_inicial.status_code}")
        print(f"Total de produtos iniciais: {len(r_lista_inicial.json())}")

        #POST  

        print_separador("POST /produtos (Cadastrar 'Cadeira de Escritório')")
        produto_novo_1 = {"nome": "Cadeira de Escritório", "categoria": "Móveis", "preco": 899.90}
        r_post_1 = httpx.post(f"{BASE_URL}/produtos", json=produto_novo_1)
        print(f"Status: {r_post_1.status_code}")
        print(r_post_1.json())
        novo_id_1 = r_post_1.json()['id']

        #GET

        print_separador(f"GET /produtos/{novo_id_1} (Buscar Cadeira)")
        r_get_id = httpx.get(f"{BASE_URL}/produtos/{novo_id_1}")
        print(f"Status: {r_get_id.status_code}")
        print(r_get_id.json())

        #PUT

        print_separador(f"PUT /produtos/{novo_id_1} (Atualizar Cadeira)")
        produto_atualizado = {"nome": "Cadeira Ergonômica", "categoria": "Móveis Premium", "preco": 1050.0}
        r_put = httpx.put(f"{BASE_URL}/produtos/{novo_id_1}", json=produto_atualizado)
        print(f"Status: {r_put.status_code}")
        print(r_put.json())

        #BUSCA ATUALIZADA

        print_separador(f"GET /produtos/{novo_id_1} (Verificar atualização da Cadeira)")
        r_get_id_atualizado = httpx.get(f"{BASE_URL}/produtos/{novo_id_1}")
        print(f"Status: {r_get_id_atualizado.status_code}")
        print(r_get_id_atualizado.json())

        #DELETE

        print_separador(f"DELETE /produtos/{novo_id_1} (Remover Cadeira)")
        r_delete = httpx.delete(f"{BASE_URL}/produtos/{novo_id_1}")
        print(f"Status: {r_delete.status_code}")
        print(r_delete.json())

        #VERIFICA REMOCAO

        print_separador(f"GET /produtos/{novo_id_1} (Verificar remoção - Deve falhar 404)")
        r_get_id_removido = httpx.get(f"{BASE_URL}/produtos/{novo_id_1}")
        print(f"Status: {r_get_id_removido.status_code}")
        print(r_get_id_removido.json())
        
        #MEDIA PRECO
        
        print_separador("GET /produtos/stats/media-precos")
        r_media = httpx.get(f"{BASE_URL}/produtos/stats/media-precos")
        print(f"Status: {r_media.status_code}")
        print(r_media.json())

        #MAIOR PRECO

        print_separador("GET /produtos/stats/maior-preco")
        r_maior = httpx.get(f"{BASE_URL}/produtos/stats/maior-preco")
        print(f"Status: {r_maior.status_code}")        
        dados_maior = r_maior.json()
        print(f"Produto de maior preço: {dados_maior['nome']} (Preço: R$ {dados_maior['preco']})")

        #MENOR PRECO

        print_separador("GET /produtos/stats/menor-preco")
        r_menor = httpx.get(f"{BASE_URL}/produtos/stats/menor-preco")
        print(f"Status: {r_menor.status_code}")
        dados_menor = r_menor.json()
        print(f"Produto de menor preço: {dados_menor['nome']} (Preço: R$ {dados_menor['preco']})")

        #ACIMA DA MEDIA

        print_separador("GET /produtos/stats/acima-media")
        r_acima = httpx.get(f"{BASE_URL}/produtos/stats/acima-media")
        print(f"Status: {r_acima.status_code}")
        print(f"Total de produtos acima da média: {len(r_acima.json())}")
        # print(r_acima.json()) # Descomente se quiser ver a lista longa

        #ABAIXO DA MEDIA

        print_separador("GET /produtos/stats/abaixo-media")
        r_abaixo = httpx.get(f"{BASE_URL}/produtos/stats/abaixo-media")
        print(f"Status: {r_abaixo.status_code}")
        print(f"Total de produtos abaixo da média: {len(r_abaixo.json())}")
        # print(r_abaixo.json()) # Descomente se quiser ver a lista longa

    except httpx.ConnectError:
        print(f"\n[ERRO] Não foi possível conectar ao servidor em {BASE_URL}")
        print("Verifique se o 'main.py' está rodando.")
    except Exception as e:
        print(f"\n[ERRO INESPERADO] {e}")

if __name__ == "__main__":
    testar_cliente()
