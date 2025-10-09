#!/bin/bash
# Script para preparar projeto para GitHub

echo "🚀 Preparando projeto para GitHub..."

# Criar arquivo .streamlit/secrets.toml.example (sem chaves reais)
mkdir -p .streamlit
cat > .streamlit/secrets.toml.example << 'EOF'
# Template de configuração de secrets
# NO STREAMLIT CLOUD, configure em: App Settings > Secrets

ANTHROPIC_API_KEY = "sua_chave_aqui"
EOF

# Criar arquivo de configuração do Streamlit
cat > .streamlit/config.toml << 'EOF'
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
enableCORS = false
port = 8501
EOF

# Atualizar .gitignore para incluir secrets
cat >> .gitignore << 'EOF'

# Streamlit Secrets (NUNCA commitar!)
.streamlit/secrets.toml

# Local development
.env
*.log
EOF

echo "✅ Projeto preparado!"
echo ""
echo "Próximo passo: git init e push para GitHub"
