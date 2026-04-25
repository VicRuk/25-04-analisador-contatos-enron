from vertice import Vertice

class Grafo:
    def __init__(self):
        self.vertices = []
        self.email_para_id = {}
        self.id_para_email = []
        self.num_vertices = 0

    def obter_ou_criar_id(self, email):
        # Recebe um e-mail e retorna seu id. Se o e-mail ainda não existe no grafo, ele é adicionado e recebe um novo id
        if email not in self.email_para_id:
            novo_id = self.num_vertices
            self.email_para_id[email] = novo_id
            self.id_para_email.append(email)
            self.vertices.append(Vertice(novo_id, email))
            self.num_vertices += 1
        return self.email_para_id[email]

    def adicionar_mensagem(self, remetente, destinatario):
        id_remetente = self.obter_ou_criar_id(remetente)
        id_destinatario = self.obter_ou_criar_id(destinatario)
        self.vertices[id_remetente].adicionar_ou_incrementar_adjacencia(id_destinatario)

    # O número de vértices do grafo é o número de e-mails únicos encontrados
    def obter_vertices(self):
        return self.num_vertices
    
    # O n. de arestas do grafo é a soma das adjacências de cada vértice
    def obter_arestas(self):
        num_arestas = sum(len(v.adjacencias) for v in self.vertices)
        return num_arestas

    # O grau de saída de um vértice é a soma dos pesos das suas adjacências
    def top_20_grau_saida(self):
        graus = []
        for v in self.vertices:
            # Soma os pesos de todas as arestas que saem deste vértice
            grau_saida = sum(aresta.peso for aresta in v.adjacencias)
            graus.append((v.informacao, grau_saida))
        
        # Ordena de forma decrescente
        graus.sort(key=lambda x: x[1], reverse=True)
        return graus[:20]

    # O grau de entrada de um vértice é a soma dos pesos das arestas que chegam nele
    def top_20_grau_entrada(self):
        # Inicializa um vetor com zeros para contar os graus de entrada de todos os vértices
        grau_entrada = [0] * self.num_vertices

        for v in self.vertices:
            for aresta in v.adjacencias:
                grau_entrada[aresta.destino] += aresta.peso

        # Monta a lista combinando o email do vértice com seu grau de entrada calculado
        graus = [(self.id_para_email[i], grau_entrada[i]) for i in range(self.num_vertices)]

        # Ordena de forma decrescente
        graus.sort(key=lambda x: x[1], reverse=True)
        return graus[:20]

    # Busca em Profundidade (DFS - Depth First Search) 
    # Explora um caminho até o fim antes de retroceder (backtracking).
    def buscar_caminho_dfs(self, email_origem, email_destino):
        if email_origem not in self.email_para_id or email_destino not in self.email_para_id:
            return None

        id_inicio = self.email_para_id[email_origem]
        id_fim = self.email_para_id[email_destino] 
        visitados = set() # Guardar os nós já visitados e evitar loops infinitos
        caminho = []

        def dfs_recursivo(atual):
            # Se o nó já foi visitado, para
            if atual in visitados:
                return False
            visitados.add(atual)
            caminho.append(atual)

            # Chegou no destino?
            if atual == id_fim:
                return True

            # Explora os vizinhos (adjacentes) do nó atual
            for aresta in self.vertices[atual].adjacencias:
                if dfs_recursivo(aresta.destino):
                    return True

            # Backtracking: se chegou num beco sem saída, remove o nó do caminho e retorna False
            caminho.pop()
            return False

        if dfs_recursivo(id_inicio):
            # Converte os ids numéricos de volta para os e-mails
            return [self.id_para_email[no] for no in caminho]
        return None
    
    # Busca em Largura (BFS - Breadth First Search)
    # Explora todos os nós de um determinado nível antes de passar para o próximo nível.
    def buscar_caminho_bfs(self, email_origem, email_destino):
        if email_origem not in self.email_para_id or email_destino not in self.email_para_id:
            return None

        id_inicio = self.email_para_id[email_origem]
        id_fim = self.email_para_id[email_destino]

        visitados = {id_inicio}
        fila = [[id_inicio]] # Fila armazenará os caminhos percorridos até o momento

        while fila:
            caminho = fila.pop(0) # Remove o primeiro caminho da fila (FIFO)
            atual = caminho[-1] # Último nó do caminho retirado

            # Se encontrou o destino, retorna o caminho convertido para e-mails
            if atual == id_fim:
                return [self.id_para_email[no] for no in caminho]

            # Percorre todos os vizinhos do nó atual
            for aresta in self.vertices[atual].adjacencias:
                if aresta.destino not in visitados:
                    visitados.add(aresta.destino)
                    novo_caminho = list(caminho)
                    novo_caminho.append(aresta.destino)
                    fila.append(novo_caminho)
        return None

    def nos_distancia_d(self, email_origem, d):
        # Retorna todos os nós que estão exatamente a uma distância 'd' arestas do nó de origem.
        if email_origem not in self.email_para_id:
            return []

        id_inicio = self.email_para_id[email_origem]
        visitados = {id_inicio}
        fila = [(id_inicio, 0)]
        resultado = []

        while fila:
            atual, dist = fila.pop(0)
            
            # Se a distância do nó atual chegou em 'd', guarda ele, sem olhar os filhos
            if dist == d:
                resultado.append(self.id_para_email[atual])
                continue

            # Se não, Continua expandindo a busca
            if dist < d:
                for aresta in self.vertices[atual].adjacencias:
                    if aresta.destino not in visitados:
                        visitados.add(aresta.destino)
                        fila.append((aresta.destino, dist + 1))
        return resultado
    
    # Em vez de buscar a menor distância pura, prioriza as arestas com maiores pesos (maior dependência).
    def caminho_critico_dijkstra(self, email_origem, email_destino):
        if email_origem not in self.email_para_id or email_destino not in self.email_para_id:
            return float('inf'), []

        s = self.email_para_id[email_origem]
        t = self.email_para_id[email_destino]

        INFINITO = float('inf')
        distancia = [INFINITO] * self.num_vertices # Vetor para armazenar as menores distâncias encontradas desde a origem
        perm = [False] * self.num_vertices # Vetor se já teve seu caminho mínimo/crítico fechado definitivamente
        caminho = [-1] * self.num_vertices # Vetor para montar a rota (guarda qual nó veio antes de qual)

        distancia[s] = 0
        corrente = s

        # O laço roda até processar o destino ou não ter mais caminhos possíveis
        while corrente != t and corrente != -1:
            perm[corrente] = True
            dc = distancia[corrente]

            # Analisa as saídas do nó atual
            for aresta in self.vertices[corrente].adjacencias:
                i = aresta.destino
                
                # Se o destino ainda não foi permanentemente resolvido
                if not perm[i]:
                    # Adaptação Dijkstra: Inverso do peso
                    # Quanto MAIOR o peso original (frequência de e-mails), MENOR será o custo, fazendo o algoritmo naturalmente escolher as rotas de conexão mais forte.
                    custo_adaptado = 1.0 / aresta.peso
                    novadist = dc + custo_adaptado

                    # Se a nova distância calculada for menor que a que já existia lá, atualiza
                    if novadist < distancia[i]:
                        distancia[i] = novadist
                        caminho[i] = corrente
            
            # Escolhe o próximo nó para processar: aquele que tiver a menor distância acumulada e que ainda não está em perm
            menordist = INFINITO
            k = -1
            for i in range(self.num_vertices):
                if not perm[i] and distancia[i] < menordist:
                    menordist = distancia[i]
                    k = i
            corrente = k

        # Remonta a rota percorrida consultando o vetor caminho de trás pra frente
        rota = []
        if distancia[t] != INFINITO:
            atual = t
            while atual != -1:
                rota.insert(0, self.id_para_email[atual])
                atual = caminho[atual]
                
        return distancia[t], rota