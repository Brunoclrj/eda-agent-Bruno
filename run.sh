#!/bin/bash
# Script de Setup e Execução do Agente EDA

echo "🤖 Agente EDA - Setup"
echo "===================="

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.11+"
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
    echo "✅ Ambiente virtual criado"
else
    echo "✅ Ambiente virtual já existe"
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "📥 Instalando dependências..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo "✅ Dependências instaladas"

# Verificar .env
if [ ! -f ".env" ]; then
    echo "⚠️  Arquivo .env não encontrado!"
    echo "📝 Criando .env a partir do .env.example..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANTE: Edite o arquivo .env e adicione sua ANTHROPIC_API_KEY"
    echo "   1. Obtenha a chave em: https://console.anthropic.com/"
    echo "   2. Edite .env e substitua 'sua_chave_anthropic_aqui'"
    echo ""
    read -p "Pressione ENTER depois de configurar o .env..."
fi

# Verificar se API key está configurada
if grep -q "sua_chave_anthropic_aqui" .env; then
    echo "❌ ANTHROPIC_API_KEY ainda não foi configurada no .env"
    echo "   Por favor, edite o arquivo .env e adicione sua chave"
    exit 1
fi

echo "✅ Configuração completa!"
echo ""
echo "🚀 Iniciando aplicação Streamlit..."
echo "   Acesse: http://localhost:8501"
echo ""

streamlit run src/ui/app.py
