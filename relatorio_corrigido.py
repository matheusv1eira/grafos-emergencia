#!/usr/bin/env python3
"""
Geração do relatório PDF CORRIGIDO (sem caracteres Unicode problemáticos)
"""

from fpdf import FPDF
import pandas as pd
import os
from datetime import datetime

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Relatorio de Experimentos em Grafos - UNIFBV', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')
    
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)
    
    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        # Substituir caracteres problemáticos
        body_safe = body.replace('•', '-')
        self.multi_cell(0, 8, body_safe)
        self.ln()

def generate_report():
    print("GERANDO RELATORIO PDF CORRIGIDO...")
    
    pdf = PDFReport()
    pdf.add_page()
    
    # Capa
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 40, 'RELATORIO DE EXPERIMENTOS CIENTIFICOS', 0, 1, 'C')
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 20, 'Busca em Grafos Planos para Resposta a Emergencias', 0, 1, 'C')
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, 'Disciplina: Algoritmos em Grafos', 0, 1, 'C')
    pdf.cell(0, 10, f'Data: {datetime.now().strftime("%d/%m/%Y %H:%M")}', 0, 1, 'C')
    pdf.ln(30)
    
    pdf.add_page()
    
    # Metodologia
    pdf.chapter_title('1. METODOLOGIA')
    methodology = """
Ferramentas utilizadas: Python 3, NetworkX, OSMnx
Base de dados: malha viaria de cidades brasileiras extraidas via OSMnx
Algoritmos testados: BFS, Dijkstra e A*

Etapas do experimento:
1. Modelagem da rede como grafo planar ponderado
2. Implementacao dos algoritmos de busca
3. Execucao de experimentos com multiplos pares origem-destino
4. Medicao de tempo de CPU e uso de memoria
5. Comparacao dos resultados
"""
    pdf.chapter_body(methodology)
    
    # Tentar carregar resultados
    try:
        df = pd.read_csv('results/tabelas/resumo_corrigido.csv')
        
        pdf.add_page()
        pdf.chapter_title('2. RESULTADOS OBTIDOS')
        
        # Tabela de resultados
        pdf.set_font('Arial', 'B', 10)
        col_widths = [40, 30, 30, 30, 30]
        headers = ['Cidade', 'Algoritmo', 'Tempo(s)', 'Distancia(m)', 'Sucessos']
        
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 10, header, 1, 0, 'C')
        pdf.ln()
        
        pdf.set_font('Arial', '', 8)
        for _, row in df.iterrows():
            pdf.cell(col_widths[0], 10, str(row['cidade']), 1, 0, 'C')
            pdf.cell(col_widths[1], 10, str(row['algoritmo']), 1, 0, 'C')
            pdf.cell(col_widths[2], 10, f"{row['tempo_cpu']:.4f}", 1, 0, 'C')
            pdf.cell(col_widths[3], 10, f"{row['distancia_total']:.1f}", 1, 0, 'C')
            pdf.cell(col_widths[4], 10, f"{row['sucesso']:.0f}", 1, 0, 'C')
            pdf.ln()
            
    except FileNotFoundError:
        pdf.chapter_body("Execute primeiro: python3 main_corrigido.py")
        pdf.chapter_body("OU execute: python3 teste_corrigido.py para um teste rapido")
    
    # Conclusão
    pdf.add_page()
    pdf.chapter_title('3. CONCLUSÃO')
    conclusao = """
Este experimento comparou tres algoritmos de busca em grafos aplicados a redes viarias urbanas:

BFS (Busca em Largura): Mais rapido mas produz rotas subotimas
Dijkstra: Garante otimalidade com custo computacional moderado  
A*: Balanceia eficiencia e qualidade usando heuristica

Os resultados demonstram a importancia da escolha do algoritmo adequado para sistemas de resposta a emergencias, onde o equilibrio entre tempo de calculo e qualidade da rota e crucial.
"""
    pdf.chapter_body(conclusao)
    
    # Salvar PDF
    output_file = 'Relatorio_Grafos_UNIFBV_Corrigido.pdf'
    pdf.output(output_file)
    print(f"RELATORIO PDF GERADO: {output_file}")

if __name__ == "__main__":
    generate_report()
