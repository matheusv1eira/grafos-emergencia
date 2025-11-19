import time
import psutil
import os
from memory_profiler import memory_usage
from typing import List, Dict, Tuple
import pandas as pd
from src.algorithms import GraphAlgorithms
import networkx as nx

class ExperimentRunner:
    def __init__(self):
        self.results = []
    
    def run_single_experiment(self, G: nx.Graph, source: int, target: int, algorithm: str) -> Dict:
        """Executa um único experimento com um algoritmo"""
        algorithm_map = {
            "BFS": GraphAlgorithms.bfs_path,
            "DIJKSTRA": GraphAlgorithms.dijkstra_path,
            "ASTAR": GraphAlgorithms.astar_path
        }
        
        if algorithm not in algorithm_map:
            raise ValueError(f"Algoritmo não suportado: {algorithm}")
        
        # Medir tempo de CPU
        start_time = time.time()
        
        # Medir uso de memória
        mem_usage = memory_usage(
            (algorithm_map[algorithm], (G, source, target)), 
            interval=0.1, 
            timeout=60
        )
        
        path, visited_nodes, nodes_expanded = algorithm_map[algorithm](G, source, target)
        end_time = time.time()
        
        # Calcular métricas
        cpu_time = end_time - start_time
        max_memory = max(mem_usage) if mem_usage else 0
        path_distance = GraphAlgorithms.calculate_path_distance(G, path)
        
        return {
            'algorithm': algorithm,
            'source': source,
            'target': target,
            'cpu_time': cpu_time,
            'memory_mb': max_memory,
            'nodes_expanded': nodes_expanded,
            'path_length': len(path) if path else 0,
            'path_distance': path_distance,
            'visited_nodes': len(visited_nodes),
            'success': len(path) > 0 and path[0] == source and path[-1] == target
        }
    
    def run_comparison(self, G: nx.Graph, source: int, target: int, algorithms: List[str]) -> List[Dict]:
        """Executa comparação entre múltiplos algoritmos"""
        results = []
        for algo in algorithms:
            try:
                result = self.run_single_experiment(G, source, target, algo)
                results.append(result)
            except Exception as e:
                print(f"Erro no algoritmo {algo}: {e}")
                results.append({
                    'algorithm': algo,
                    'source': source,
                    'target': target,
                    'cpu_time': 0,
                    'memory_mb': 0,
                    'nodes_expanded': 0,
                    'path_length': 0,
                    'path_distance': 0,
                    'visited_nodes': 0,
                    'success': False,
                    'error': str(e)
                })
        return results
    
    def run_scalability_test(self, G: nx.Graph, sizes: List[int], algorithm: str) -> List[Dict]:
        """Testa escalabilidade com diferentes tamanhos de grafo"""
        from src.data_loader import DataLoader
        loader = DataLoader()
        
        results = []
        for size in sizes:
            if size > len(G.nodes):
                continue
                
            subgraph = loader.create_subgraph(G, size)
            if len(subgraph.nodes) < 2:
                continue
            
            # Escolher nós aleatórios para teste
            import random
            nodes = list(subgraph.nodes())
            source = random.choice(nodes)
            target = random.choice(nodes)
            
            while source == target and len(nodes) > 1:
                target = random.choice(nodes)
            
            try:
                result = self.run_single_experiment(subgraph, source, target, algorithm)
                result['graph_size'] = size
                results.append(result)
            except Exception as e:
                print(f"Erro no tamanho {size}: {e}")
        
        return results
