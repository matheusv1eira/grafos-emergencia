import networkx as nx
import heapq
import math
from typing import List, Tuple, Dict, Set
import time

class GraphAlgorithms:
    @staticmethod
    def bfs_path(G: nx.Graph, source: int, target: int) -> Tuple[List[int], Set[int], int]:
        """Busca em Largura - retorna caminho, nós visitados e contagem de expansões"""
        if source == target:
            return [source], {source}, 0
        
        queue = [(source, [source])]
        visited = {source}
        nodes_expanded = 0
        
        while queue:
            nodes_expanded += 1
            current, path = queue.pop(0)
            
            for neighbor in G.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    
                    if neighbor == target:
                        return new_path, visited, nodes_expanded
                    
                    queue.append((neighbor, new_path))
        
        return [], visited, nodes_expanded
    
    @staticmethod
    def dijkstra_path(G: nx.Graph, source: int, target: int) -> Tuple[List[int], Set[int], int]:
        """Dijkstra - retorna caminho mínimo baseado em distância"""
        if source == target:
            return [source], {source}, 0
        
        distances = {node: float('inf') for node in G.nodes()}
        distances[source] = 0
        previous = {node: None for node in G.nodes()}
        visited = set()
        nodes_expanded = 0
        
        pq = [(0, source)]
        
        while pq:
            nodes_expanded += 1
            current_dist, current = heapq.heappop(pq)
            
            if current in visited:
                continue
                
            visited.add(current)
            
            if current == target:
                # Reconstruir caminho
                path = []
                while current is not None:
                    path.append(current)
                    current = previous[current]
                return path[::-1], visited, nodes_expanded
            
            for neighbor in G.neighbors(current):
                if neighbor not in visited:
                    edge_data = G.get_edge_data(current, neighbor)
                    if edge_data:
                        length = edge_data.get('length', 1)
                        new_dist = current_dist + length
                        
                        if new_dist < distances[neighbor]:
                            distances[neighbor] = new_dist
                            previous[neighbor] = current
                            heapq.heappush(pq, (new_dist, neighbor))
        
        return [], visited, nodes_expanded
    
    @staticmethod
    def astar_path(G: nx.Graph, source: int, target: int) -> Tuple[List[int], Set[int], int]:
        """A* com heurística euclidiana"""
        if source == target:
            return [source], {source}, 0
        
        def heuristic(u, v):
            """Heurística euclidiana baseada em coordenadas"""
            if 'x' in G.nodes[u] and 'y' in G.nodes[u] and 'x' in G.nodes[v] and 'y' in G.nodes[v]:
                dx = G.nodes[u]['x'] - G.nodes[v]['x']
                dy = G.nodes[u]['y'] - G.nodes[v]['y']
                return math.sqrt(dx*dx + dy*dy)
            return 0
        
        g_score = {node: float('inf') for node in G.nodes()}
        g_score[source] = 0
        f_score = {node: float('inf') for node in G.nodes()}
        f_score[source] = heuristic(source, target)
        
        previous = {node: None for node in G.nodes()}
        visited = set()
        nodes_expanded = 0
        
        open_set = [(f_score[source], source)]
        
        while open_set:
            nodes_expanded += 1
            _, current = heapq.heappop(open_set)
            
            if current in visited:
                continue
                
            visited.add(current)
            
            if current == target:
                # Reconstruir caminho
                path = []
                while current is not None:
                    path.append(current)
                    current = previous[current]
                return path[::-1], visited, nodes_expanded
            
            for neighbor in G.neighbors(current):
                if neighbor not in visited:
                    edge_data = G.get_edge_data(current, neighbor)
                    if edge_data:
                        length = edge_data.get('length', 1)
                        tentative_g = g_score[current] + length
                        
                        if tentative_g < g_score[neighbor]:
                            previous[neighbor] = current
                            g_score[neighbor] = tentative_g
                            f_score[neighbor] = tentative_g + heuristic(neighbor, target)
                            heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        return [], visited, nodes_expanded
    
    @staticmethod
    def calculate_path_distance(G: nx.Graph, path: List[int]) -> float:
        """Calcula distância total de um caminho"""
        if len(path) < 2:
            return 0
        
        total_distance = 0
        for i in range(len(path) - 1):
            edge_data = G.get_edge_data(path[i], path[i + 1])
            if edge_data and 'length' in edge_data:
                total_distance += edge_data['length']
        
        return total_distance
