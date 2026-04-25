import os
import email
import re
from grafo import Grafo

_RE_EMAIL = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")

def extrair_emails(campo):
    if not campo:
        return []
    return [e.lower() for e in _RE_EMAIL.findall(campo)]

def carregar_dados(grafo, pasta_raiz):
    print(f"[*] Lendo e-mails da pasta: '{pasta_raiz}'...")
    total = 0

    for raiz, _, arquivos in os.walk(pasta_raiz):
        for nome in arquivos:
            if nome.startswith('.') or nome.startswith('._'):
                continue
            
            caminho = os.path.join(raiz, nome)
            try:
                with open(caminho, 'rb') as f:
                    msg = email.message_from_bytes(f.read())
            except Exception:
                continue

            remetentes = extrair_emails(msg.get('From', ''))
            if not remetentes:
                continue
            remetente = remetentes[0]

            destinatarios = []
            for campo in ('To', 'Cc', 'Bcc'):
                destinatarios.extend(extrair_emails(msg.get(campo, '')))

            for dest in set(destinatarios):
                # Ignora auto-envio
                if dest != remetente: 
                    grafo.adicionar_mensagem(remetente, dest)
            total += 1

    print(f"[*] Processo concluído! {total} e-mails lidos.\n")

def main():
    print("ANALISADOR DE CONTATOS ENRON")

    # Buscar arquivo
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    pasta_amostra = os.path.join(diretorio_atual, "Amostra Enron")

    if not os.path.exists(pasta_amostra):
        print(f"ERRO: A pasta '{pasta_amostra}' não foi encontrada.")
        return

    grafo = Grafo()
    carregar_dados(grafo, pasta_amostra)


    print("INFORMAÇÕES GERAIS")
    # 2a) N. de vértices do grafo
    qtd_v = grafo.obter_vertices()
    print(f"Número de Vértices: {qtd_v}")

    # 2b) N. de arestas do grafo
    qtd_a = grafo.obter_arestas()
    print(f"Número de Arestas: {qtd_a}\n")
    
    # 2c) Top 20 indivíduos que possuem maior grau de saída e o valor correspondente
    print("Top 20 Indivíduos (Maior Grau de Saída):")
    for i, (usr, grau) in enumerate(grafo.top_20_grau_saida(), 1):
        print(f"   {i}. {usr} ({grau})")
        
    # 2d) Top 20 indivíduos que possuem maior grau de entrada e o valor correspondente
    print("\nd. Top 20 Indivíduos (Maior Grau de Entrada):")
    for i, (usr, grau) in enumerate(grafo.top_20_grau_entrada(), 1):
        print(f"   {i}. {usr} ({grau})")

    # Teste de rotas
    top_saida = grafo.top_20_grau_saida()
    if len(top_saida) < 2:
        print("\nNão há vértices suficientes para testar as rotas.")
        return
        
    origem = top_saida[0][0]
    destino = top_saida[1][0]
    
    print("\n" + "="*60)
    print(f"TESTANDO ROTAS ENTRE: {origem} -> {destino}")
    print("="*60)

    # 3) Percorre o grafo em PROFUNDIDADE e verifica se um indivíduo X pode alcançar um indivíduo Y retornando e mostrando o caminho percorrido (nós visitados) em uma lista.
    print(f"\nBusca em PROFUNDIDADE:")
    rota_dfs = grafo.buscar_caminho_dfs(origem, destino)
    if rota_dfs:
        print(" -> ".join(rota_dfs))
    else:
        print("Nenhum caminho encontrado.")

    # 4) Percorre o grafo em LARGURA e verifica se um indivíduo X pode alcançar um indivíduo Y retornando e mostrando o caminho percorrido (nós visitados) em uma lista.
    print(f"\nBusca em LARGURA:")
    rota_bfs = grafo.buscar_caminho_bfs(origem, destino)
    if rota_bfs:
        print(" -> ".join(rota_bfs))
    else:
        print("Nenhum caminho encontrado.")

    # 5) Retorna uma lista com os nós que estão a uma distância de D arestas de um nó N. Considere que uma ligação entre os nós X e Y corresponde a uma distância 1 entre X e Y. 
    D = 2
    print(f"\nNós a uma distância exata de D = {D} de {origem}:")
    nos_distantes = grafo.nos_distancia_d(origem, D)
    print(f"Encontrados {len(nos_distantes)} nós. Exibindo até 10: {nos_distantes[:10]}")

    # 6) Adaptação no algoritmo Dijkstra para que ele considere o inverso do peso das arestas 
    print(f"\nCaminho Crítico (Dijkstra Adaptado - Inverso do peso):")
    custo, rota_critica = grafo.caminho_critico_dijkstra(origem, destino)
    if custo != float('inf'):
        print(f"Custo Adaptado: {custo:.4f}")
        print(" -> ".join(rota_critica))
    else:
        print("Nenhum caminho crítico possível.")
        
    print("\n" + "="*60)

if __name__ == "__main__":
    main()