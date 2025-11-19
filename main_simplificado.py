#!/usr/bin/env python3
"""
Script principal simplificado para experimentos
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

import pandas as pd
import numpy as np
from config import CITIES, ALGORITHMS
import osmnx as ox
import networkx as nx
import time
from memory_profiler import memory_usage

def calcular_caminho(G, origem, destino, algoritmo):
    """Calcula caminho usando algoritmo específico"""
    if algoritmo == "BFS":
        return nx.shortest_path(G, origem, destino)
    elif algoritmo == "DIJKSTRA":
        return nx.shortest_path(G, origem, destino, weight='length')
    elif algoritmo == "ASTAR":
        return nx.astar_path(G, origem, destino, weight='length')
    else:
        raise ValueError(f"Algoritmo não suportado: {algoritmo}")

def calcular_distancia(G, caminho):
    """Calcula distância total de um caminho"""
    if len(caminho) < 2:
        return 0
    distancia = 0
    for i in range(len(caminho)-1):
        edge_data = G.get_edge_data(caminho[i], caminho[i+1])
        if edge_data is not None:
            # Pega o primeiro dicionário de atributos (pode haver múltiplas arestas em grafos não direcionados)
            key = list(edge_data.keys())[0]
            distancia += edge_data[key].get('length', 0)
    return distancia

def main():
    print("🚀 INICIANDO EXPERIMENTOS SIMPLIFICADOS")
    
    resultados = []
    
    for cidade in CITIES:
        print(f"\n🏙️  Processando: {cidade}")
        
        try:
            # Carregar grafo
            G = ox.graph_from_place(cidade, network_type='drive', simplify=True)
            G = G.to_undirected()
            G = ox.add_edge_lengths(G)
            
            print(f"✅ Grafo carregado: {len(G.nodes)} nós")
            
            # Escolher alguns pares de nós para teste
            nodes = list(G.nodes())
            pares_teste = []
            
            for i in range(min(5, len(nodes)//2)):
                origem = nodes[i]
                destino = nodes[-(i+1)]
                pares_teste.append((origem, destino))
            
            # Testar cada algoritmo em cada par
            for origem, destino in pares_teste:
                for algoritmo in ALGORITHMS:
                    try:
                        # Medir tempo e memória
                        inicio_tempo = time.time()
                        
                        def executar_algoritmo():
                            return calcular_caminho(G, origem, destino, algoritmo)
                        
                        # Medir uso de memória
                        uso_memoria = memory_usage(executar_algoritmo, interval=0.1, timeout=30)
                        tempo_execucao = time.time() - inicio_tempo
                        
                        # Calcular caminho novamente para obter resultado
                        caminho = executar_algoritmo()
                        distancia = calcular_distancia(G, caminho)
                        
                        resultado = {
                            'cidade': cidade.split(',')[0],
                            'algoritmo': algoritmo,
                            'origem': origem,
                            'destino': destino,
                            'tempo_cpu': tempo_execucao,
                            'memoria_mb': max(uso_memoria) if uso_memoria else 0,
                            'nos_expandidos': len(caminho),
                            'distancia_total': distancia,
                            'sucesso': True
                        }
                        
                        resultados.append(resultado)
                        print(f"✅ {algoritmo}: {tempo_execucao:.4f}s, {distancia:.1f}m")
                        
                    except Exception as e:
                        print(f"❌ Erro em {algoritmo}: {e}")
                        resultados.append({
                            'cidade': cidade.split(',')[0],
                            'algoritmo': algoritmo,
                            'origem': origem,
                            'destino': destino,
                            'tempo_cpu': 0,
                            'memoria_mb': 0,
                            'nos_expandidos': 0,
                            'distancia_total': 0,
                            'sucesso': False,
                            'erro': str(e)
                        })
            
        except Exception as e:
            print(f"❌ Erro ao processar {cidade}: {e}")
    
    # Salvar resultados
    if resultados:
        df = pd.DataFrame(resultados)
        df.to_csv('results/tabelas/resultados_simplificados.csv', index=False)
        
        # Estatísticas resumidas
        resumo = df.groupby(['cidade', 'algoritmo']).agg({
            'tempo_cpu': 'mean',
            'memoria_mb': 'mean',
            'distancia_total': 'mean',
            'sucesso': 'sum'
        }).reset_index()
        
        resumo.to_csv('results/tabelas/resumo_simplificado.csv', index=False)
        
        print(f"\n📊 RESULTADOS SALVOS:")
        print(f"   - results/tabelas/resultados_simplificados.csv")
        print(f"   - results/tabelas/resumo_simplificado.csv")
        
        print("\n📋 RESUMO:")
        print(resumo.round(4))
    
    print("\n✅ EXPERIMENTOS CONCLUÍDOS!")

if __name__ == "__main__":
    main()
