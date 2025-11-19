#!/usr/bin/env python3
"""
Script de teste CORRIGIDO para a versão atual do OSMnx
"""

import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import time
import pandas as pd

print("🧪 INICIANDO TESTE CORRIGIDO")

# Configurações básicas
ox.settings.log_console = True
ox.settings.use_cache = True

try:
    # Testar carregamento de uma cidade pequena
    print("1. Carregando grafo do Recife...")
    G = ox.graph_from_place("Recife, Brazil", network_type='drive', simplify=True)
    
    # Converter para não-direcionado (forma correta para versão atual)
    G = ox.utils_graph.get_undirected(G) if hasattr(ox, 'utils_graph') else G.to_undirected()
    
    # Adicionar comprimentos (forma correta)
    if hasattr(ox, 'distance') and hasattr(ox.distance, 'add_edge_lengths'):
        G = ox.distance.add_edge_lengths(G)
    else:
        # Alternativa para versões mais recentes
        G = ox.add_edge_lengths(G)
    
    print(f"✅ Grafo carregado: {len(G.nodes)} nós, {len(G.edges)} arestas")
    
    # Escolher dois pontos
    nodes = list(G.nodes())
    origem = nodes[0]
    destino = nodes[-1]
    
    print(f"2. Testando algoritmos entre nó {origem} e {destino}")
    
    resultados = []
    
    # Função para calcular distância
    def calcular_distancia_caminho(G, caminho):
        distancia = 0
        for i in range(len(caminho) - 1):
            edge_data = G.get_edge_data(caminho[i], caminho[i + 1])
            if edge_data and 'length' in list(edge_data.values())[0]:
                distancia += list(edge_data.values())[0]['length']
        return distancia
    
    # Teste BFS
    print("   - BFS...")
    inicio = time.time()
    try:
        caminho_bfs = nx.shortest_path(G, origem, destino)
        tempo_bfs = time.time() - inicio
        distancia_bfs = calcular_distancia_caminho(G, caminho_bfs)
        resultados.append({'Algoritmo': 'BFS', 'Tempo(s)': tempo_bfs, 'Distancia(m)': distancia_bfs})
    except Exception as e:
        print(f"      ❌ Erro no BFS: {e}")
        resultados.append({'Algoritmo': 'BFS', 'Tempo(s)': 0, 'Distancia(m)': 0})
    
    # Teste Dijkstra
    print("   - Dijkstra...")
    inicio = time.time()
    try:
        caminho_dijkstra = nx.shortest_path(G, origem, destino, weight='length')
        tempo_dijkstra = time.time() - inicio
        distancia_dijkstra = calcular_distancia_caminho(G, caminho_dijkstra)
        resultados.append({'Algoritmo': 'Dijkstra', 'Tempo(s)': tempo_dijkstra, 'Distancia(m)': distancia_dijkstra})
    except Exception as e:
        print(f"      ❌ Erro no Dijkstra: {e}")
        resultados.append({'Algoritmo': 'Dijkstra', 'Tempo(s)': 0, 'Distancia(m)': 0})
    
    # Teste A*
    print("   - A*...")
    inicio = time.time()
    try:
        caminho_astar = nx.astar_path(G, origem, destino, weight='length')
        tempo_astar = time.time() - inicio
        distancia_astar = calcular_distancia_caminho(G, caminho_astar)
        resultados.append({'Algoritmo': 'A*', 'Tempo(s)': tempo_astar, 'Distancia(m)': distancia_astar})
    except Exception as e:
        print(f"      ❌ Erro no A*: {e}")
        resultados.append({'Algoritmo': 'A*', 'Tempo(s)': 0, 'Distancia(m)': 0})
    
    # Mostrar resultados
    df = pd.DataFrame(resultados)
    print("\n📊 RESULTADOS DO TESTE:")
    print(df)
    
    # Salvar resultados
    df.to_csv('results/tabelas/teste_corrigido.csv', index=False)
    
    # Criar gráfico simples
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.bar(df['Algoritmo'], df['Tempo(s)'], color=['red', 'green', 'blue'])
    plt.title('Tempo de Execução (s)')
    plt.ylabel('Segundos')
    
    plt.subplot(1, 2, 2)
    plt.bar(df['Algoritmo'], df['Distancia(m)'], color=['red', 'green', 'blue'])
    plt.title('Distância do Caminho (m)')
    plt.ylabel('Metros')
    
    plt.tight_layout()
    plt.savefig('results/figuras/teste_corrigido.png', dpi=300, bbox_inches='tight')
    print("✅ Gráfico salvo: results/figuras/teste_corrigido.png")
    
    print("\n🎯 TESTE CONCLUÍDO COM SUCESSO!")
    
except Exception as e:
    print(f"❌ Erro durante o teste: {e}")
    import traceback
    traceback.print_exc()
