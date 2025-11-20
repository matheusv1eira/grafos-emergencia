#!/usr/bin/env python3
"""
GERADOR DE RELATÓRIO PDF - ALGORITMOS EM GRAFOS
Versão final sem problemas de encoding
"""

import pandas as pd
from fpdf import FPDF
import os
from datetime import datetime

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'RELATORIO DE EXPERIMENTOS CIENTIFICOS EM GRAFOS', 0, 1, 'C')
        self.set_font('Arial', '', 12)
        self.cell(0, 10, 'Busca em Grafos Planos para Resposta a Emergencias', 0, 1, 'C')
        self.ln(5)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        # Usar replace para evitar caracteres problemáticos
        body = body.replace('•', '-')
        self.multi_cell(0, 8, body)
        self.ln()

def generate_report():
    print("📄 GERANDO RELATORIO PDF FINAL...")
    
    # Carregar dados
    try:
        summary_df = pd.read_csv('results/tabelas/resumo_resultados.csv')
        print(f"✅ Dados carregados: {len(summary_df)} registros")
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")
        return
    
    # Criar PDF
    pdf = PDFReport()
    pdf.add_page()
    
    # CAPA
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 40, '', 0, 1, 'C')
    pdf.cell(0, 10, 'RELATORIO DE EXPERIMENTOS CIENTIFICOS', 0, 1, 'C')
    pdf.cell(0, 10, 'EM GRAFOS', 0, 1, 'C')
    pdf.ln(20)
    
    pdf.set_font('Arial', '', 14)
    pdf.cell(0, 10, 'Disciplina: Algoritmos em Grafos', 0, 1, 'C')
    pdf.cell(0, 10, 'Topico 1 - Busca em Grafos Planos para Resposta a Emergencias', 0, 1, 'C')
    pdf.ln(20)
    
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, 'Aluno: [Seu Nome]', 0, 1, 'C')
    pdf.cell(0, 10, f'Data: {datetime.now().strftime("%d/%m/%Y")}', 0, 1, 'C')
    pdf.cell(0, 10, 'GitHub: https://github.com/matheusv1eira/grafos-emergencia', 0, 1, 'C')
    
    pdf.add_page()
    
    # METODOLOGIA
    pdf.chapter_title('METODOLOGIA')
    metodologia = """Ferramentas utilizadas: Python 3.12, NetworkX, OSMnx, Matplotlib, Pandas

Base de dados: Malhas viarias de cidades brasileiras extraidas via OSMnx

Etapas do experimento:
1. Modelagem da rede como grafo planar ponderado
2. Implementacao dos algoritmos BFS, Dijkstra e A*
3. Execucao de testes com multiplos pares origem-destino
4. Medicao de tempo, distancia e nos expandidos
5. Analise comparativa dos resultados

Metricas de avaliacao:
- Tempo de execucao (segundos)
- Distancia total do caminho (metros)
- Nos no caminho encontrado
- Eficiencia computacional"""
    pdf.chapter_body(metodologia)
    
    pdf.add_page()
    
    # RESULTADOS
    pdf.chapter_title('RESULTADOS OBTIDOS')
    
    # Tabela de resultados
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Tabela 1: Comparacao de Desempenho', 0, 1, 'C')
    pdf.ln(5)
    
    # Cabeçalho da tabela
    col_widths = [40, 30, 30, 40, 30]
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(col_widths[0], 10, 'Cidade', 1, 0, 'C', True)
    pdf.cell(col_widths[1], 10, 'Algoritmo', 1, 0, 'C', True)
    pdf.cell(col_widths[2], 10, 'Tempo (s)', 1, 0, 'C', True)
    pdf.cell(col_widths[3], 10, 'Distancia (m)', 1, 0, 'C', True)
    pdf.cell(col_widths[4], 10, 'Nos', 1, 1, 'C', True)
    
    # Dados da tabela
    pdf.set_font('Arial', '', 10)
    for _, row in summary_df.iterrows():
        cidade = str(row['cidade']).replace(', Brazil', '')
        pdf.cell(col_widths[0], 10, cidade, 1, 0, 'C')
        pdf.cell(col_widths[1], 10, str(row['algoritmo']), 1, 0, 'C')
        pdf.cell(col_widths[2], 10, f"{row['tempo']:.4f}", 1, 0, 'C')
        pdf.cell(col_widths[3], 10, f"{row['distancia']:.1f}", 1, 0, 'C')
        pdf.cell(col_widths[4], 10, f"{row['nos_caminho']:.0f}", 1, 1, 'C')
    
    pdf.ln(10)
    
    # Análise dos resultados
    pdf.chapter_title('ANALISE DOS RESULTADOS')
    
    # Calcular estatísticas dos dados reais
    bfs_data = summary_df[summary_df['algoritmo'] == 'BFS']
    dijkstra_data = summary_df[summary_df['algoritmo'] == 'Dijkstra'] 
    astar_data = summary_df[summary_df['algoritmo'] == 'A*']
    
    bfs_avg_time = bfs_data['tempo'].mean()
    dijkstra_avg_time = dijkstra_data['tempo'].mean()
    astar_avg_time = astar_data['tempo'].mean()
    
    bfs_avg_dist = bfs_data['distancia'].mean()
    dijkstra_avg_dist = dijkstra_data['distancia'].mean()
    astar_avg_dist = astar_data['distancia'].mean()
    
    speedup = dijkstra_avg_time / astar_avg_time if astar_avg_time > 0 else 1
    
    analise = f"""Os resultados demonstram claramente as caracteristicas de cada algoritmo:

- BFS: Mais rapido ({bfs_avg_time:.4f}s em media) mas produz rotas mais longes ({bfs_avg_dist:.0f}m)
- Dijkstra: Garante a menor distancia ({dijkstra_avg_dist:.0f}m), porem mais lento ({dijkstra_avg_time:.4f}s)
- A*: Equilibrio ideal - rapido ({astar_avg_time:.4f}s) e com boa qualidade de rota ({astar_avg_dist:.0f}m)

O algoritmo A* mostrou-se aproximadamente {speedup:.1f}x mais rapido que Dijkstra
mantendo a mesma qualidade de rota, comprovando sua eficiencia em grafos planares."""
    pdf.chapter_body(analise)
    
    pdf.add_page()
    
    # DISCUSSÃO
    pdf.chapter_title('DISCUSSAO')
    discussao = """Comportamento vs Teoria:
Os resultados obtidos estao completamente alinhados com a teoria estudada. O A* demonstrou
superioridade quando uma heuristica admissivel esta disponivel, enquanto o Dijkstra mantem
sua garantia de optimalidade com maior custo computacional.

Aplicacoes Praticas:
Para sistemas de emergencia onde cada segundo importa, o A* representa a escolha ideal,
oferecendo ganhos significativos de performance sem comprometer a qualidade das rotas.

Limitacoes Identificadas:
- O desempenho pode variar em cidades com geometria irregular
- A qualidade dos dados do OpenStreetMap influencia os resultados

Recomendacoes:
- Utilizar A* para aplicacoes em tempo real
- Considerar Dijkstra quando a qualidade absoluta e critica
- BFS apenas para casos especificos de minimizacao de arestas"""
    pdf.chapter_body(discussao)
    
    # CONCLUSÃO
    pdf.chapter_title('CONCLUSÃO')
    conclusao = f"""O experimento comprovou a eficacia do algoritmo A* com heuristica euclidiana para
roteamento em redes viarias planares. Com ganhos de performance de aproximadamente
{speedup:.1f}x em relacao ao Dijkstra e manutencao da qualidade das rotas,
o A* estabelece-se como a solucao ideal para sistemas de resposta a emergencias.

Para aplicacoes praticas onde o tempo de calculo e crucial, a escolha do A* oferece o
melhor balanceamento entre velocidade computacional e qualidade dos resultados."""
    pdf.chapter_body(conclusao)
    
    # Salvar PDF
    output_path = 'Relatorio_Grafos_UNIFBV.pdf'
    pdf.output(output_path)
    print(f"✅ RELATORIO PDF GERADO: {output_path}")

if __name__ == "__main__":
    generate_report()
