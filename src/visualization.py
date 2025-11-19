import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
from typing import Dict

class ResultVisualizer:
    def __init__(self, output_dir="results/figuras"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        plt.style.use('seaborn-v0_8')
    
    def plot_algorithm_comparison(self, df: pd.DataFrame, city_name: str):
        """Gráfico de comparação entre algoritmos"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'Comparação de Algoritmos - {city_name}', fontsize=16)
        
        # Tempo de CPU
        sns.barplot(data=df, x='algorithm', y='cpu_time', ax=axes[0,0])
        axes[0,0].set_title('Tempo de CPU (s)')
        axes[0,0].set_ylabel('Segundos')
        
        # Uso de Memória
        sns.barplot(data=df, x='algorithm', y='memory_mb', ax=axes[0,1])
        axes[0,1].set_title('Uso de Memória (MB)')
        axes[0,1].set_ylabel('MB')
        
        # Nós Expandidos
        sns.barplot(data=df, x='algorithm', y='nodes_expanded', ax=axes[1,0])
        axes[1,0].set_title('Nós Expandidos')
        axes[1,0].set_ylabel('Quantidade')
        
        # Distância do Caminho
        sns.barplot(data=df, x='algorithm', y='path_distance', ax=axes[1,1])
        axes[1,1].set_title('Distância do Caminho (m)')
        axes[1,1].set_ylabel('Metros')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/comparacao_algoritmos_{city_name.split(",")[0]}.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_scalability(self, scalability_data: Dict, algorithm: str):
        """Gráfico de escalabilidade"""
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle(f'Escalabilidade - {algorithm}', fontsize=16)
        
        sizes = []
        times = []
        memories = []
        
        for size, metrics in scalability_data.items():
            sizes.append(size)
            times.append(np.mean(metrics['cpu_time']))
            memories.append(np.mean(metrics['memory_mb']))
        
        # Tempo vs Tamanho
        axes[0].plot(sizes, times, 'o-', linewidth=2, markersize=8)
        axes[0].set_xlabel('Tamanho do Grafo (nós)')
        axes[0].set_ylabel('Tempo CPU (s)')
        axes[0].set_title('Tempo vs Tamanho')
        axes[0].grid(True, alpha=0.3)
        
        # Memória vs Tamanho
        axes[1].plot(sizes, memories, 'o-', linewidth=2, markersize=8, color='orange')
        axes[1].set_xlabel('Tamanho do Grafo (nós)')
        axes[1].set_ylabel('Memória (MB)')
        axes[1].set_title('Memória vs Tamanho')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/escalabilidade_{algorithm}.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_summary_table(self, all_results: Dict) -> pd.DataFrame:
        """Cria tabela sumária dos resultados"""
        summary_data = []
        
        for city, results in all_results.items():
            df_city = pd.DataFrame(results)
            for algo in df_city['algorithm'].unique():
                df_algo = df_city[df_city['algorithm'] == algo]
                summary_data.append({
                    'Cidade': city.split(',')[0],
                    'Algoritmo': algo,
                    'Tempo_Medio_s': df_algo['cpu_time'].mean(),
                    'Memoria_Media_MB': df_algo['memory_mb'].mean(),
                    'Nos_Expandidos_Medio': df_algo['nodes_expanded'].mean(),
                    'Distancia_Media_m': df_algo['path_distance'].mean(),
                    'Sucesso_%': (df_algo['success'].sum() / len(df_algo)) * 100
                })
        
        return pd.DataFrame(summary_data)
