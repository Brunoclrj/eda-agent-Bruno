# 🚀 Guia Rápido de Início

## Instalação em 3 Passos

### 1️⃣ Instalar Dependências

```bash
# Linux/Mac
./run.sh

# OU manualmente:
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### 2️⃣ Configurar API Key

```bash
# Copiar template
cp .env.example .env

# Editar .env e adicionar sua chave:
# ANTHROPIC_API_KEY=sk-ant-...
```

**Onde conseguir a chave:**
1. Acesse: https://console.anthropic.com/
2. Login/Cadastro
3. API Keys → Create Key
4. Copie e cole no .env

### 3️⃣ Executar

```bash
streamlit run src/ui/app.py
```

Acesse: http://localhost:8501

---

## Uso Rápido

1. **Upload CSV** (barra lateral)
2. **Faça perguntas** (aba "Fazer Perguntas")
3. **Veja conclusões** (aba "Memória & Conclusões")

### Exemplos de Perguntas

```
"Descreva a distribuição das variáveis numéricas"
"Mostre um heatmap de correlação"
"Existem outliers? Mostre um boxplot"
"Há tendência temporal?"
"Quais as principais conclusões?"
```

---

## Troubleshooting

**Erro: ANTHROPIC_API_KEY não configurada**
→ Verifique o arquivo .env

**Erro ao instalar dependências**
→ Use Python 3.11+

**Erro ChromaDB**
→ Delete `data/memory/` e reinicie

---

## Deploy Rápido (Link Público)

### Streamlit Cloud (Grátis)

1. Suba para GitHub
2. Acesse https://streamlit.io/cloud
3. Conecte repositório
4. Adicione secret: `ANTHROPIC_API_KEY`
5. Deploy!

Link será gerado automaticamente.

---

## Estrutura Mínima

```
eda-agent/
├── src/
│   ├── agent/eda_agent.py       # Agente
│   ├── tools/                   # CSV, EDA, Plots
│   ├── memory/                  # Sistema de memória
│   └── ui/app.py                # Interface
├── requirements.txt
├── .env                         # Suas configs
└── README.md
```

---

## Próximos Passos

1. ✅ Executar aplicação
2. ✅ Testar com CSV de fraudes
3. ✅ Fazer ≥4 perguntas (≥1 com gráfico)
4. ✅ Perguntar sobre conclusões
5. ✅ Gerar relatório PDF
6. ✅ Deploy (link público)
7. ✅ Enviar para challenges@i2a2.academy

---

**Pronto para começar? Execute:**

```bash
./run.sh
```
