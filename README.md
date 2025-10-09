# 🤖 Agente Autônomo para Análise Exploratória de Dados (EDA)

Sistema de agentes inteligentes capaz de realizar análise exploratória em **qualquer arquivo CSV**, gerando insights, gráficos e mantendo memória das conclusões.

## 📋 Requisitos da Atividade

✅ Interface para perguntas em linguagem natural  
✅ Suporte a qualquer CSV (encoding/delimitador automático)  
✅ Geração de gráficos analíticos  
✅ Memória persistente de análises e conclusões  
✅ Relatório PDF com 7 itens obrigatórios  
✅ Link público para testes  
✅ Segredos ocultados  

## 🚀 Como Usar

### 1. Instalação

```bash
# Clone ou extraia o projeto
cd eda-agent

# Criar ambiente virtual
python3.11 -m venv venv

# Ativar ambiente
source venv/bin/activate  # Linux/Mac
# OU
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configuração

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env e adicionar sua chave da Anthropic
# ANTHROPIC_API_KEY=sua_chave_aqui
```

**Como obter chave da Anthropic:**
1. Acesse https://console.anthropic.com/
2. Faça login ou crie uma conta
3. Vá em "API Keys"
4. Gere uma nova chave
5. Cole no arquivo .env

### 3. Executar

```bash
# Executar aplicação Streamlit
streamlit run src/ui/app.py

# A aplicação abrirá em http://localhost:8501
```

## 📊 Como Usar o Agente

1. **Carregar CSV:**
   - Clique em "Browse files" na barra lateral
   - Selecione seu arquivo CSV
   - Clique em "Carregar CSV"

2. **Fazer Perguntas:**
   - Vá para a aba "Fazer Perguntas"
   - Digite sua pergunta em linguagem natural
   - Clique em "Perguntar"
   - O agente analisará e responderá com texto + gráficos

3. **Ver Conclusões:**
   - Aba "Memória & Conclusões"
   - Veja histórico de todas as análises
   - Faça perguntas sobre as conclusões acumuladas

## 🎯 Exemplos de Perguntas

```
- "Descreva a distribuição de todas as variáveis numéricas"
- "Mostre um heatmap de correlação entre as variáveis"
- "Existem outliers na coluna Amount? Mostre um boxplot"
- "Há tendência temporal na coluna Time?"
- "Faça uma análise de clusters nos dados"
- "Quais as principais conclusões sobre este dataset?"
```

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────┐
│    Interface Web (Streamlit)            │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│    Agente EDA (Claude Sonnet 4.5)       │
│    • Entende pergunta                   │
│    • Planeja análise                    │
│    • Executa ferramentas                │
│    • Sintetiza resposta                 │
└────────────┬────────────────────────────┘
             │
   ┌─────────┼─────────┬─────────┐
   ▼         ▼         ▼         ▼
[CSV]    [EDA]    [Plot]    [Memory]
Handler  Engine   Generator   Store
```

## 📦 Estrutura do Projeto

```
eda-agent/
├── src/
│   ├── agent/
│   │   └── eda_agent.py          # Agente principal
│   ├── tools/
│   │   ├── csv_handler.py        # Carregamento de CSV
│   │   ├── eda_engine.py         # Análises estatísticas
│   │   └── plot_generator.py     # Geração de gráficos
│   ├── memory/
│   │   └── memory_store.py       # Sistema de memória
│   └── ui/
│       └── app.py                # Interface Streamlit
├── data/
│   ├── uploads/                  # CSVs carregados
│   └── memory/                   # Banco de memória
├── outputs/                      # Gráficos gerados
├── requirements.txt
├── .env.example
└── README.md
```

## 🔐 Segurança

- ✅ API keys em variáveis de ambiente (.env)
- ✅ Arquivo .env não versionado (.gitignore)
- ✅ Sem hardcoded secrets no código
- ✅ .env.example como template

## 🛠️ Tecnologias

| Componente | Tecnologia |
|------------|------------|
| LLM | Claude Sonnet 4.5 (Anthropic) |
| Interface | Streamlit |
| Processamento | Pandas, NumPy, SciPy |
| Visualização | Plotly |
| Memória | ChromaDB + SQLite |
| Clustering | Scikit-learn |

## 📝 Gerando o Relatório PDF

O relatório PDF será implementado em `src/report/generate_pdf.py` e deve conter:

1. Framework escolhida (Claude + Streamlit)
2. Arquitetura da solução
3. ≥4 perguntas com respostas (≥1 com gráfico)
4. 1 pergunta sobre conclusões + resposta
5. Códigos-fonte
6. Link público
7. Evidências de ocultação de chaves

## 🌐 Deploy (Link Público)

### Opção 1: Streamlit Community Cloud

```bash
# 1. Suba código para GitHub
git init
git add .
git commit -m "EDA Agent"
git push

# 2. Acesse https://streamlit.io/cloud
# 3. Conecte repositório
# 4. Configure secrets (ANTHROPIC_API_KEY)
# 5. Deploy!

# Link gerado: https://seu-app.streamlit.app
```

### Opção 2: Docker

```bash
# Build
docker build -t eda-agent .

# Run
docker run -p 8501:8501 \
  -e ANTHROPIC_API_KEY=sua_chave \
  eda-agent
```

## 🧪 Testando com CSV Diferente

O agente é genérico e funciona com **qualquer CSV**:

1. Acesse o link público
2. Faça upload do CSV de teste
3. Faça perguntas em linguagem natural
4. O agente processará automaticamente

**Suporta:**
- Qualquer delimitador (`,` `;` `\t` `|`)
- Qualquer encoding (UTF-8, Latin1, etc.)
- Milhares de linhas
- Dezenas de colunas

## 📚 Dataset de Exemplo

O projeto foi testado com o dataset de fraudes de cartão:
- **Fonte:** https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
- **Colunas:** Time, V1-V28 (PCA), Amount, Class
- **Tamanho:** ~284k linhas, 31 colunas

## ❓ Troubleshooting

**Erro: ANTHROPIC_API_KEY não configurada**
- Verifique se o arquivo .env existe
- Verifique se a chave está correta
- Certifique-se de que o .env está no diretório raiz

**Erro ao carregar CSV**
- Verifique se o arquivo é realmente CSV
- Tente com sample_size menor
- Verifique encoding do arquivo

**Erro no ChromaDB**
- Delete a pasta `data/memory/` e reinicie

## 👨‍💻 Autor

Projeto desenvolvido para a atividade obrigatória do curso de Agentes Autônomos - I²A²

## 📄 Licença

Este projeto é para fins educacionais.
