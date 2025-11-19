#!/usr/bin/env python3
"""
Script principal CORRIGIDO para experimentos
"""

import pandas as pd
import osmnx as ox
import networkx as nx
import time
from memory_profiler import memory_usage
import random

print("🚀 INICIANDO EXPERIMENTOS CORRIGIDOS")

# Configurações
CITIES = ["Recife, Brazil"]  # Começar com apenas uma cidade
ALGORITHMS = ["BFS", "DIJKSTRA", "ASTAR"]

def calcular_caminho(G, origem, destino, algoritmo):
    """Calcula caminho usando algoritmo específico"""
    try:
        if algoritmo == "BFS":
            return nx.shortest_path(G, origem, destino)
        elif algoritmo == "DIJKSTRA":
            return nx.shortest_path(G, origem, destino, weight='length')
        elif algoritmo == "ASTAR":
            return nx.astar_path(G, origem, destino, weight='length')
    except Exception as e:
        print(f"      ❌ Erro no {algoritmo}: {e}")
        return []
    return []

def calcular_distancia(G, caminho):
    """Calcula distância total de um caminho"""
    if len(caminho) < 2:
        return 0
    
    distancia = 0
    for i in range(len(caminho) - 1):
        edge_data = G.get_edge_data(caminho[i], caminho[i + 1])
        if edge_data:
            # Pega o primeiro dicionário de atributos (pode haver múltiplas arestas)
            first_edge = list(edge_data.values())[0]
            if 'length' in first_edge:
                distancia += first_edge['length']
    return distancia

resultados = []

for cidade in CITIES:
    print(f"\n🏙️  Processando: {cidade}")
    
    try:
        # Carregar grafo
        print("   - Carregando grafo...")
        G = ox.graph_from_place(cidade, network_type='drive', simplify=True)
        
        # Converter para não-direcionado
        if hasattr(ox, 'utils_graph'):
            G = ox.utils_graph.get_undirected(G)
        else:
            G = G.to_undirected()
        
        # Adicionar comprimentos
        if hasattr(ox, 'distance') and hasattr(ox.distance, 'add_edge_lengths'):
            G = ox.distance.add_edge_lengths(G)
        else:
            G = ox.add_edge_lengths(G)
        
        print(f"   ✅ Grafo carregado: {len(G.nodes)} nós")
        
        # Escolher alguns pares de nós para teste
        nodes = list(G.nodes())
        pares_teste = []
        
        num_pares = min(3, len(nodes) // 10)  # Número reduzido para teste
        for i in range(num_pares):
            origem = random.choice(nodes)
            destino = random.choice(nodes)
            # Garantir que origem e destino são diferentes
            tentativas = 0
            while origem == destino and tentativas < 10:
                destino = random.choice(nodes)
                tentativas += 1
            if origem != destino:
                pares_teste.append((origem, destino))
        
        print(f"   - Testando {len(pares_teste)} pares...")
        
        # Testar cada algoritmo em cada par
        for idx, (origem, destino) in enumerate(pares_teste):
            print(f"     Par {idx+1}: {origem} → {destino}")
            
            for algoritmo in ALGORITHMS:
                try:
                    # Medir tempo
                    inicio_tempo = time.time()
                    
                    # Executar algoritmo
                    caminho = calcular_caminho(G, origem, destino, algoritmo)
                    
                    tempo_execucao = time.time() - inicio_tempo
                    
                    if caminho:
                        distancia = calcular_distancia(G, caminho)
                        
                        resultado = {
                            'cidade': cidade.split(',')[0],
                            'algoritmo': algoritmo,
                            'tempo_cpu': tempo_execucao,
                            'distancia_total': distancia,
                            'nos_caminho': len(caminho),
                            'sucesso': True
                        }
                        
                        resultados.append(resultado)
                        print(f"       ✅ {algoritmo}: {tempo_execucao:.4f}s, {distancia:.1f}m")
                    else:
                        resultados.append({
                            'cidade': cidade.split(',')[0],
                            'algoritmo': algoritmo,
                            'tempo_cpu': 0,
                            'distancia_total': 0,
                            'nos_caminho': 0,
                            'sucesso': False
                        })
                        print(f"       ❌ {algoritmo}: falhou")
                        
                except Exception as e:
                    print(f"       ❌ Erro em {algoritmo}: {e}")
                    resultados.append({
                        'cidade': cidade.split(',')[0],
                        'algoritmo': algoritmo,
                        'tempo_cpu': 0,
                        'distancia_total': 0,
                        'nos_caminho': 0,
                        'sucesso': False,
                        'erro': str(e)
                    })
            
    except Exception as e:
        print(f"❌ Erro ao processar {cidade}: {e}")

# Salvar resultados
if resultados:
    df = pd.DataFrame(resultados)
    df.to_csv('results/tabelas/resultados_corrigidos.csv', index=False)
    
    # Estatísticas resumidas
    resumo = df.groupby(['cidade', 'algoritmo']).agg({
        'tempo_cpu': 'mean',
        'distancia_total': 'mean',
        'sucesso': 'sum'
    }).reset_index()
    
    resumo.to_csv('results/tabelas/resumo_corrigido.csv', index=False)
    
    print(f"\n📊 RESULTADOS SALVOS:")
    print(f"   - results/tabelas/resultados_corrigidos.csv")
    print(f"   - results/tabelas/resumo_corrigido.csv")
    
    print("\n📋 RESUMO:")
    print(resumo.round(4))
    
    # Gráfico simples
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    
    for i, algoritmo in enumerate(ALGORITHMS):
        dados_algo = resumo[resumo['algoritmo'] == algoritmo]
        if not dados_algo.empty:
            plt.bar(i, dados_algo['tempo_cpu'].values[0], label=algoritmo, 
                   color=['red', 'green', 'blue'][i])
    
    plt.xlabel('Algoritmo')
    plt.ylabel('Tempo Médio (s)')
    plt.title('Comparação de Tempo de Execução')
    plt.xticks(range(len(ALGORITHMS)), ALGORITHMS)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('results/figuras/comparacao_tempo.png', dpi=300, bbox_inches='tight')
    print("   - results/figuras/comparacao_tempo.png")

print("\n✅ EXPERIMENTOS CONCLUÍDOS!")
