#!/usr/bin/env python3
"""
Script principal para experimentos de busca em grafos planos
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

import pandas as pd
import numpy as np
from config import CITIES, ALGORITHMS, NUM_EXPERIMENTS, GRAPH_SIZE_TESTS
from src.data_loader import DataLoader
from src.experiment_runner import ExperimentRunner
from src.visualization import ResultVisualizer
import networkx as nx

def main():
    print("🚀 INICIANDO EXPERIMENTOS DE BUSCA EM GRAFOS PLANOS")
    print("=" * 60)
    
    # Inicializar componentes
    loader = DataLoader()
    runner = ExperimentRunner()
    visualizer = ResultVisualizer()
    
    all_results = {}
    scalability_results = {}
    
    for city in CITIES:
        print(f"\n🏙️  PROCESSANDO CIDADE: {city}")
        print("-" * 40)
        
        # Carregar grafo da cidade
        G = loader.load_city_graph(city)
        if G is None:
            print(f"❌ Não foi possível carregar grafo para {city}")
            continue
        
        # Obter pontos de interesse
        hospitals = loader.get_poi_coordinates(city, "hospital")
        schools = loader.get_poi_coordinates(city, "school")
        
        print(f"🏥 Hospitais encontrados: {len(hospitals)}")
        print(f"🏫 Escolas encontradas: {len(schools)}")
        
        if len(hospitals) == 0 or len(schools) == 0:
            print("❌ Pontos de interesse insuficientes")
            continue
        
        # Converter coordenadas para nós do grafo
        hospital_nodes = [loader.find_nearest_node(G, coord) for coord in hospitals[:5]]
        school_nodes = [loader.find_nearest_node(G, coord) for coord in schools[:5]]
        
        city_results = []
        
        # Executar experimentos para pares hospital-escola
        for i, hospital in enumerate(hospital_nodes):
            for j, school in enumerate(school_nodes):
                if hospital != school:
                    print(f"🔍 Teste {i+1}-{j+1}: Hospital {hospital} → Escola {school}")
                    
                    results = runner.run_comparison(G, hospital, school, ALGORITHMS)
                    for result in results:
                        result['city'] = city
                        result['test_id'] = f"{i+1}-{j+1}"
                    
                    city_results.extend(results)
        
        all_results[city] = city_results
        
        # Teste de escalabilidade para cada algoritmo
        print(f"\n📈 TESTANDO ESCALABILIDADE EM {city.split(',')[0]}")
        for algorithm in ALGORITHMS:
            print(f"   Algoritmo: {algorithm}")
            scalability_data = runner.run_scalability_test(G, GRAPH_SIZE_TESTS, algorithm)
            
            if city not in scalability_results:
                scalability_results[city] = {}
            scalability_results[city][algorithm] = scalability_data
    
    # Gerar visualizações e resultados
    print("\n📊 GERANDO RESULTADOS E GRÁFICOS")
    
    # Tabela sumária
    summary_df = visualizer.create_summary_table(all_results)
    summary_df.to_csv('results/tabelas/resumo_resultados.csv', index=False)
    
    print("\n" + "="*60)
    print("📋 RESUMO DOS RESULTADOS")
    print("="*60)
    print(summary_df.round(4))
    
    # Gráficos para cada cidade
    for city, results in all_results.items():
        df_city = pd.DataFrame(results)
        city_name_short = city.split(',')[0]
        visualizer.plot_algorithm_comparison(df_city, city_name_short)
        
        # Salvar resultados detalhados
        df_city.to_csv(f'results/tabelas/detalhes_{city_name_short}.csv', index=False)
    
    # Gráficos de escalabilidade
    for city, algo_data in scalability_results.items():
        for algorithm, data in algo_data.items():
            if data:
                df_scalability = pd.DataFrame(data)
                scalability_metrics = {}
                for size in GRAPH_SIZE_TESTS:
                    size_data = df_scalability[df_scalability['graph_size'] == size]
                    if len(size_data) > 0:
                        scalability_metrics[size] = {
                            'cpu_time': size_data['cpu_time'].tolist(),
                            'memory_mb': size_data['memory_mb'].tolist()
                        }
                visualizer.plot_scalability(scalability_metrics, f"{algorithm}_{city.split(',')[0]}")
    
    print("\n✅ EXPERIMENTOS CONCLUÍDOS!")
    print("📁 Resultados salvos em:")
    print("   - results/tabelas/")
    print("   - results/figuras/")

if __name__ == "__main__":
    main()
