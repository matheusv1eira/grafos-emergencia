import networkx as nx
import matplotlib.pyplot as plt
import time
import pandas as pd
import os

print("🎯 SOLUÇÃO FINAL - Teste Ultra-Simplificado")

# Criar diretórios
os.makedirs("results/tabelas", exist_ok=True)
os.makedirs("results/figuras", exist_ok=True)

# Criar um grafo simples de teste (SEM OSMnx)
G = nx.erdos_renyi_graph(100, 0.1, seed=42)

# Adicionar pesos aleatórios simulando distâncias
for (u, v) in G.edges():
    G[u][v]['length'] = round(abs(hash(str((u, v)))) % 100 + 1, 2)

resultados = []

# Escolher nós
origem = 0
destino = 99

print(f"Testando em grafo sintético: {len(G.nodes)} nós, {len(G.edges())} arestas")
print(f"Origem: {origem}, Destino: {destino}")

# ---------- BFS ----------
inicio = time.time()
try:
    caminho_bfs = nx.shortest_path(G, origem, destino)
    tempo_bfs = time.time() - inicio
    dist_bfs = sum(G[u][v]['length'] for u, v in zip(caminho_bfs[:-1], caminho_bfs[1:]))
    
    resultados.append({
        'Algoritmo': 'BFS',
        'Tempo(s)': tempo_bfs,
        'Distancia': dist_bfs,
        'Nos': len(caminho_bfs)
    })

    print(f"✅ BFS: {tempo_bfs:.6f}s, {dist_bfs:.2f} unidades, {len(caminho_bfs)} nós")
except Exception as e:
    print(f"❌ BFS falhou: {e}")

# ---------- Dijkstra ----------
inicio = time.time()
try:
    caminho_dijkstra = nx.shortest_path(G, origem, destino, weight='length')
    tempo_dijkstra = time.time() - inicio
    dist_dijkstra = sum(G[u][v]['length'] for u, v in zip(caminho_dijkstra[:-1], caminho_dijkstra[1:]))

    resultados.append({
        'Algoritmo': 'Dijkstra',
        'Tempo(s)': tempo_dijkstra,
        'Distancia': dist_dijkstra,
        'Nos': len(caminho_dijkstra)
    })

    print(f"✅ Dijkstra: {tempo_dijkstra:.6f}s, {dist_dijkstra:.2f} unidades, {len(caminho_dijkstra)} nós")
except Exception as e:
    print(f"❌ Dijkstra falhou: {e}")

# ---------- A* ----------
inicio = time.time()
try:
    caminho_astar = nx.astar_path(G, origem, destino, weight='length')
    tempo_astar = time.time() - inicio
    dist_astar = sum(G[u][v]['length'] for u, v in zip(caminho_astar[:-1], caminho_astar[1:]))

    resultados.append({
        'Algoritmo': 'A*',
        'Tempo(s)': tempo_astar,
        'Distancia': dist_astar,
        'Nos': len(caminho_astar)
    })

    print(f"✅ A*: {tempo_astar:.6f}s, {dist_astar:.2f} unidades, {len(caminho_astar)} nós")
except Exception as e:
    print(f"❌ A* falhou: {e}")

# ---------- Salvar Resultados ----------
if resultados:
    df = pd.DataFrame(resultados)
    df.to_csv('results/tabelas/solucao_final.csv', index=False)

    # ----- Gráficos -----
    plt.figure(figsize=(12, 4))

    # Gráfico 1
    plt.subplot(1, 3, 1)
    plt.bar(df['Algoritmo'], df['Tempo(s)'])
    plt.title('Tempo de Execução')
    plt.ylabel('Segundos')

    # Gráfico 2
    plt.subplot(1, 3, 2)
    plt.bar(df['Algoritmo'], df['Distancia'])
    plt.title('Distância do Caminho')
    plt.ylabel('Unidades')

    # Gráfico 3
    plt.subplot(1, 3, 3)
    plt.bar(df['Algoritmo'], df['Nos'])
    plt.title('Nós no Caminho')
    plt.ylabel('Quantidade')

    plt.tight_layout()
    plt.savefig('results/figuras/solucao_final.png', dpi=300)

    print("\n📊 RESULTADOS:")
    print(df)

    print("\n💾 Arquivos salvos:")
    print("   - results/tabelas/solucao_final.csv")
    print("   - results/figuras/solucao_final.png")

    print("\n🎉 SOLUÇÃO FINAL CONCLUÍDA COM SUCESSO!")
else:
    print("❌ Nenhum algoritmo funcionou. Verifique o ambiente.")
