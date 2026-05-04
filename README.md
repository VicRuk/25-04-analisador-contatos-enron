# Analisador de Contatos Enron - TDE3

Integrantes do grupo:
- Gustavo Lazzari
- Mateus Roese
- Matheus Yamamoto
- Victor Ryuki

Projeto referente à matéria *Resolução de Problemas com Grafos* que constrói um grafo direcionado e ponderado a partir do dataset de e-mails da Enron, mapeando as relações de comunicação entre funcionários. O programa realiza análise de grau de entrada e saída, busca em profundidade (DFS), busca em largura (BFS), alcance por distância e cálculo de caminho crítico via Dijkstra adaptado.

## 1. Como executar

Antes de executar, certifique-se de que a pasta `Amostra Enron` com os e-mails está presente no mesmo diretório que o `main.py`.

```zsh
python main.py
```

## 2. Estrutura do Repositório

```
.
├── aresta.py      # Classe Aresta, armazena o destino e o peso de uma aresta
├── vertice.py     # Classe Vertice, armazena id, rótulo e lista de adjacências
├── grafo.py       # Classe Grafo, implementa todas as operações sobre o grafo (carregamento, análise, buscas, Dijkstra adaptado)
├── main.py        # Script principal que carrega os dados e executa todas as análises em sequência
└── README.md      
```

## 3. Operações disponíveis

- `adicionar_mensagem(remetente, destinatario)` - adiciona ou incrementa o peso da aresta entre dois endereços de e-mail
- `obter_vertices()` - retorna o número total de vértices (indivíduos únicos) no grafo
- `obter_arestas()` - retorna o número total de arestas (relações de envio) no grafo
- `top_20_grau_saida()` - retorna os 20 indivíduos com maior grau de saída (mais e-mails enviados) e os valores correspondentes
- `top_20_grau_entrada()` - retorna os 20 indivíduos com maior grau de entrada (mais e-mails recebidos) e os valores correspondentes
- `buscar_caminho_dfs(origem, destino)` - percorre o grafo em profundidade e retorna o caminho entre dois vértices como lista de nós visitados
- `buscar_caminho_bfs(origem, destino)` - percorre o grafo em largura e retorna o caminho entre dois vértices como lista de nós visitados
- `nos_distancia_d(no, d)` - retorna todos os nós que estão a exatamente `d` arestas de distância de um nó `n`
- `caminho_critico_dijkstra(origem, destino)` - calcula o caminho crítico usando Dijkstra adaptado com o inverso do peso das arestas, retornando o custo e a rota

## 4. Exemplo de uso

Saída do programa `main.py`, que lê os e-mails da pasta `Amostra Enron` e executa todas as análises:

```
ANALISADOR DE CONTATOS ENRON
[*] Lendo e-mails da pasta: 'Amostra Enron'...
[*] Processo concluído! 30109 e-mails lidos.

INFORMAÇÕES GERAIS
Número de Vértices: 1383
Número de Arestas: 8595

Top 20 Indivíduos (Maior Grau de Saída):
   1. kenneth.lay@enron.com (937)
   2. jeff.dasovich@enron.com (891)
   3. richard.shapiro@enron.com (833)
   ...

d. Top 20 Indivíduos (Maior Grau de Entrada):
   1. jeff.dasovich@enron.com (778)
   2. richard.shapiro@enron.com (703)
   3. james.steffes@enron.com (694)
   ...

============================================================
TESTANDO ROTAS ENTRE: kenneth.lay@enron.com -> jeff.dasovich@enron.com
============================================================

Busca em PROFUNDIDADE:
kenneth.lay@enron.com -> jeff.dasovich@enron.com

Busca em LARGURA:
kenneth.lay@enron.com -> jeff.dasovich@enron.com

Nós a uma distância exata de D = 2 de kenneth.lay@enron.com:
Encontrados 312 nós. Exibindo até 10: ['sara.shackleton@enron.com', ...]

Caminho Crítico (Dijkstra Adaptado - Inverso do peso):
Custo Adaptado: 0.0011
kenneth.lay@enron.com -> jeff.dasovich@enron.com

============================================================
```
