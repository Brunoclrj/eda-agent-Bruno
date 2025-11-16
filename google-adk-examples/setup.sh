#!/bin/bash
# Script de instalação do Google ADK para Linux/Mac
# Execute: bash google-adk-examples/setup.sh

set -e  # Para em caso de erro

echo "🚀 Instalando Google ADK para desenvolvimento..."
echo ""

# Verificar se está na raiz do projeto
if [ ! -f ".env.example" ]; then
    echo "❌ Erro: Execute este script na raiz do projeto eda-agent-Bruno"
    exit 1
fi

# 1. Criar ambiente virtual
echo "📦 1/4 - Criando ambiente virtual..."
if [ -d "venv-adk" ]; then
    echo "   ⚠️  venv-adk já existe, pulando..."
else
    python3 -m venv venv-adk
    echo "   ✅ Ambiente virtual criado"
fi

# 2. Ativar ambiente virtual e instalar dependências
echo ""
echo "📥 2/4 - Instalando dependências do Google ADK..."
source venv-adk/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r google-adk-examples/requirements-adk.txt
echo "   ✅ Dependências instaladas"

# 3. Configurar .env
echo ""
echo "🔑 3/4 - Configurando arquivo .env..."
if [ -f ".env" ]; then
    echo "   ⚠️  Arquivo .env já existe"
    echo "   Verifique se GOOGLE_API_KEY está configurada"
else
    cp .env.example .env
    echo "   ✅ Arquivo .env criado"
    echo "   ⚠️  IMPORTANTE: Edite o arquivo .env e adicione sua GOOGLE_API_KEY"
    echo "   Obtenha em: https://aistudio.google.com/app/apikey"
fi

# 4. Verificar instalação
echo ""
echo "🧪 4/4 - Verificando instalação..."
python -c "import google.adk; import google.genai; print('   ✅ Importações OK')" 2>&1

echo ""
echo "✨ Instalação concluída!"
echo ""
echo "📝 Próximos passos:"
echo "   1. Ative o ambiente virtual:"
echo "      source venv-adk/bin/activate"
echo ""
echo "   2. Configure sua API Key no arquivo .env:"
echo "      GOOGLE_API_KEY=sua_chave_aqui"
echo ""
echo "   3. Execute o primeiro exemplo:"
echo "      python google-adk-examples/01_basic_agent.py"
echo ""
echo "📚 Documentação completa em: google-adk-examples/QUICKSTART.md"
