from typing import List, Dict

def calculate_suboptimality(dijkstra_distance: float, other_distance: float) -> float:
    """
    Calcula o subótimo relativo em relação ao Dijkstra (considerado ótimo).
    """
    if dijkstra_distance == 0:
        return 0
    return (other_distance - dijkstra_distance) / dijkstra_distance * 100

def average_metrics(results: List[Dict]) -> Dict:
    """
    Calcula a média das métricas de uma lista de resultados.
    """
    avg = {}
    for key in results[0].keys():
        if key == 'path':
            continue
        avg[key] = sum(r[key] for r in results) / len(results)
    return avg

