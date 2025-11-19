import osmnx as ox
import networkx as nx
import pandas as pd
import numpy as np
from typing import List, Tuple, Dict
import time

class DataLoader:
    def __init__(self):
        ox.settings.log_console = True
        ox.settings.use_cache = True
        ox.settings.cache_folder = "./cache"
    
    def load_city_graph(self, city_name: str) -> nx.Graph:
        """Carrega grafo de uma cidade do OSM"""
        try:
            print(f"Carregando grafo para: {city_name}")
            G = ox.graph_from_place(city_name, network_type='drive', simplify=True)
            G = ox.utils_graph.get_undirected(G)
            G = ox.distance.add_edge_lengths(G)
            print(f"Grafo carregado: {len(G.nodes)} nós, {len(G.edges)} arestas")
            return G
        except Exception as e:
            print(f"Erro ao carregar {city_name}: {e}")
            return None
    
    def get_poi_coordinates(self, city_name: str, poi_type: str) -> List[Tuple[float, float]]:
        """Obtém coordenadas de pontos de interesse"""
        tags = {}
        if poi_type == "hospital":
            tags = {'amenity': 'hospital'}
        elif poi_type == "school":
            tags = {'amenity': 'school'}
        else:
            return []
        
        try:
            gdf = ox.geometries_from_place(city_name, tags)
            if len(gdf) == 0:
                return []
            
            # Converter para lista de coordenadas (lat, lon)
            coords = []
            for geom in gdf.geometry:
                if geom.geom_type == 'Point':
                    coords.append((geom.y, geom.x))
                elif geom.geom_type in ['Polygon', 'MultiPolygon']:
                    centroid = geom.centroid
                    coords.append((centroid.y, centroid.x))
            return coords
        except Exception as e:
            print(f"Erro ao obter POIs {poi_type} em {city_name}: {e}")
            return []
    
    def find_nearest_node(self, G: nx.Graph, point: Tuple[float, float]) -> int:
        """Encontra o nó mais próximo de uma coordenada"""
        return ox.distance.nearest_nodes(G, point[1], point[0])
    
    def create_subgraph(self, G: nx.Graph, num_nodes: int) -> nx.Graph:
        """Cria subgrafo com número específico de nós para teste de escalabilidade"""
        if len(G.nodes) <= num_nodes:
            return G.copy()
        
        nodes = list(G.nodes)[:num_nodes]
        return G.subgraph(nodes).copy()
