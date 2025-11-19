#!/usr/bin/env python3
"""
Script de teste simplificado para verificar se tudo está funcionando
"""

import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import time
import pandas as pd

print("🧪 INICIANDO TESTE SIMPLIFICADO")

# Configurações básicas
ox.settings.log_console = True
ox.settings.use_cache = True

try:
    # Testar carregamento de uma cidade pequena
    print("1. Carregando grafo do Recife...")
    G = ox.graph_from_place("Recife, Brazil", network_type='drive', simplify=True)
    # Converter para não direcionado usando NetworkX
    G = G.to_undirected()
    # Adicionar comprimentos às arestas
    G = ox.add_edge_lengths(G)

    print(f"✅ Grafo carregado: {len(G.nodes)} nós, {len(G.edges)} arestas")
    
    # Escolher dois pontos
    nodes = list(G.nodes())
    origem = nodes[0]
    destino = nodes[-1]
    
    print(f"2. Testando algoritmos entre nó {origem} e {destino}")
    
    resultados = []
    
    # Teste BFS
    inicio = time.time()
    caminho_bfs = nx.shortest_path(G, origem, destino)
    tempo_bfs = time.time() - inicio
    # Calcular a distância do caminho BFS
    distancia_bfs = 0
    for i in range(len(caminho_bfs)-1):
        edge_data = G.get_edge_data(caminho_bfs[i], caminho_bfs[i+1])
        if edge_data is not None:
            # Pega o primeiro dicionário de atributos (pode haver múltiplas arestas em grafos não direcionados)
            key = list(edge_data.keys())[0]
            distancia_bfs += edge_data[key].get('length', 0)
    resultados.append({'Algoritmo': 'BFS', 'Tempo(s)': tempo_bfs, 'Distancia(m)': distancia_bfs})
    
    # Teste Dijkstra
    inicio = time.time()
    caminho_dijkstra = nx.shortest_path(G, origem, destino, weight='length')
    tempo_dijkstra = time.time() - inicio
    distancia_dijkstra = 0
    for i in range(len(caminho_dijkstra)-1):
        edge_data = G.get_edge_data(caminho_dijkstra[i], caminho_dijkstra[i+1])
        if edge_data is not None:
            key = list(edge_data.keys())[0]
            distancia_dijkstra += edge_data[key].get('length', 0)
    resultados.append({'Algoritmo': 'Dijkstra', 'Tempo(s)': tempo_dijkstra, 'Distancia(m)': distancia_dijkstra})
    
    # Teste A*
    inicio = time.time()
    caminho_astar = nx.astar_path(G, origem, destino, weight='length')
    tempo_astar = time.time() - inicio
    distancia_astar = 0
    for i in range(len(caminho_astar)-1):
        edge_data = G.get_edge_data(caminho_astar[i], caminho_astar[i+1])
        if edge_data is not None:
            key = list(edge_data.keys())[0]
            distancia_astar += edge_data[key].get('length', 0)
    resultados.append({'Algoritmo': 'A*', 'Tempo(s)': tempo_astar, 'Distancia(m)': distancia_astar})
    
    # Mostrar resultados
    df = pd.DataFrame(resultados)
    print("\n📊 RESULTADOS DO TESTE:")
    print(df)
    
    # Salvar resultados
    df.to_csv('results/tabelas/teste_simples.csv', index=False)
    
    # Criar gráfico simples
    plt.figure(figsize=(10, 6))
    plt.subplot(1, 2, 1)
    plt.bar(df['Algoritmo'], df['Tempo(s)'])
    plt.title('Tempo de Execução')
    plt.ylabel('Segundos')
    
    plt.subplot(1, 2, 2)
    plt.bar(df['Algoritmo'], df['Distancia(m)'])
    plt.title('Distância do Caminho')
    plt.ylabel('Metros')
    
    plt.tight_layout()
    plt.savefig('results/figuras/teste_simples.png', dpi=300, bbox_inches='tight')
    print("✅ Gráfico salvo: results/figuras/teste_simples.png")
    
    print("\n🎯 TESTE CONCLUÍDO COM SUCESSO!")
    
except Exception as e:
    print(f"❌ Erro durante o teste: {e}")
    import traceback
    traceback.print_exc()
    print("💡 Dica: Verifique sua conexão com a internet para baixar dados do OSM")
