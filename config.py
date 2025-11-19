# Configurações do experimento - Versão Simplificada
CITIES = ["Recife, Brazil"]  # Começar com apenas uma cidade

ALGORITHMS = ["BFS", "DIJKSTRA", "ASTAR"]
NUM_EXPERIMENTS = 5  # Reduzir para testes
GRAPH_SIZE_TESTS = [100, 500, 1000]  # Testes menores

# Configurações OSM
OSM_SETTINGS = {
    'network_type': 'drive',
    'simplify': True
}
