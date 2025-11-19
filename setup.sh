#!/bin/bash
echo "🔧 CONFIGURANDO AMBIENTE PARA EXPERIMENTOS DE GRAFOS"

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
echo "📦 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

# Criar diretórios necessários
mkdir -p results/{figuras,tabelas,logs}
mkdir -p data/{raw,processed,points}

echo "✅ Configuração concluída!"
echo "🚀 Para executar os experimentos:"
echo "   source venv/bin/activate"
echo "   python main.py"
