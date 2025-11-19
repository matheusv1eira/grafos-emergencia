import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import time

# === Configuração da cidade ===
cidade = "Recife, Pernambuco, Brasil"
G = ox.graph_from_place(cidade, network_type='drive')

# Seleciona dois nós aleatórios do grafo
origem = list(G.nodes())[0]
destino = list(G.nodes())[-1]

# Armazena tempos
resultados = {}

# === BFS (Busca em Largura) ===
inicio = time.time()
bfs_caminho = nx.shortest_path(G, origem, destino)  # BFS padrão
fim = time.time()
resultados['BFS'] = fim - inicio

# === Dijkstra ===
inicio = time.time()
dijkstra_caminho = nx.shortest_path(G, origem, destino, weight='length', method='dijkstra')
fim = time.time()
resultados['Dijkstra'] = fim - inicio

# === A* ===
inicio = time.time()
astar_caminho = nx.astar_path(G, origem, destino, weight='length')  # <-- corrigido
fim = time.time()
resultados['A*'] = fim - inicio

# Exibe tempos
print("\n⏱️ TEMPOS DE EXECUÇÃO (em segundos):")
for alg, tempo in resultados.items():
    print(f"{alg}: {tempo:.4f}")

# Gera imagem com as rotas
fig, ax = ox.plot_graph_routes(G, [bfs_caminho, dijkstra_caminho, astar_caminho],
                               route_colors=['r', 'g', 'b'],
                               route_linewidth=2,
                               node_size=0,
                               bgcolor='white')

plt.savefig("rotas_comparativas.png", dpi=300)
print("\n🗺️ Rotas salvas no arquivo: rotas_comparativas.png")
