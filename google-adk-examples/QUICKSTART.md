# ⚡ Guia de Início Rápido - Google ADK

## 🎯 Objetivo
Configurar e executar seu primeiro agente com Google ADK em menos de 5 minutos!

## 📝 Passo a Passo

### 1️⃣ Obter API Key do Google Gemini

1. Acesse: https://aistudio.google.com/app/apikey
2. Faça login com sua conta Google
3. Clique em **"Create API Key"** ou **"Get API Key"**
4. Copie a chave gerada (formato: `AIza...`)

### 2️⃣ Configurar a Chave no Projeto

**Opção A - Usando arquivo .env (Recomendado):**

1. Abra o arquivo `.env` na raiz do projeto (se não existir, copie de `.env.example`)
2. Adicione sua chave:
   ```
   GOOGLE_API_KEY=AIzaSy...sua_chave_aqui
   ```
3. Salve o arquivo

**Opção B - Variável de ambiente temporária:**
```bash
export GOOGLE_API_KEY="AIzaSy...sua_chave_aqui"
```

### 3️⃣ Instalar Dependências (se ainda não instalou)

```bash
# Na raiz do projeto
pip install google-adk google-genai python-dotenv
```

Ou use o arquivo de requirements específico:
```bash
pip install -r google-adk-examples/requirements-adk.txt
```

### 4️⃣ Executar Primeiro Exemplo

```bash
# Execute o exemplo básico
python google-adk-examples/01_basic_agent.py
```

**Saída esperada:**
```
🤖 Criando agente básico com Google ADK...

📝 Fazendo pergunta ao agente...

 ### Created new session: debug_session_id

User > Explique em 2-3 frases o que é um agente de IA.
AssistenteBasico > Um agente de IA é um programa...

✅ Exemplo básico concluído!
```

### 5️⃣ Explorar Outros Exemplos

Agora que funcionou, explore os outros padrões:

```bash
# Multi-Agente (Pesquisa + Resumo)
python google-adk-examples/02_multi_agent_research.py

# Sequential (Pipeline)
python google-adk-examples/03_sequential_agent.py

# Parallel (Execução Simultânea)
python google-adk-examples/04_parallel_agent.py

# Loop (Refinamento Iterativo)
python google-adk-examples/05_loop_agent.py
```

## 🐛 Problemas Comuns

### ❌ Erro: "GOOGLE_API_KEY não configurada"
**Solução:**
- Verifique se adicionou a chave no `.env`
- Verifique se o nome da variável está correto: `GOOGLE_API_KEY`
- Certifique-se de que o arquivo `.env` está na raiz do projeto

### ❌ Erro: "No module named 'google.adk'"
**Solução:**
```bash
pip install google-adk google-genai
```

### ❌ Erro: "No module named 'dotenv'"
**Solução:**
```bash
pip install python-dotenv
```

### ❌ Erro 429: "Rate limit exceeded"
**Solução:**
- Você fez muitas requisições rapidamente
- Aguarde 1-2 minutos e tente novamente
- Os exemplos já têm retry automático configurado

### ❌ API Key inválida
**Solução:**
- Verifique se copiou a chave completa (sem espaços)
- Gere uma nova chave em: https://aistudio.google.com/app/apikey
- Verifique se a chave não expirou

## 📚 Próximos Passos

1. ✅ Executou o exemplo básico? → Tente o multi-agente
2. ✅ Entendeu multi-agente? → Explore sequential e parallel
3. ✅ Dominou os padrões? → Crie seu próprio agente personalizado
4. ✅ Criou algo legal? → Compartilhe com a comunidade!

## 🔗 Links Úteis

- **Documentação do ADK**: https://cloud.google.com/vertex-ai/docs/agent-builder
- **Console do Google AI**: https://aistudio.google.com/
- **Curso Kaggle**: https://www.kaggle.com/learn/agents
- **Vídeo Tutorial**: https://www.youtube.com/watch?v=ZaUcqznlhv8

## 💡 Dicas

- Use `gemini-2.5-flash-lite` para testes (rápido e barato)
- Use `gemini-2.5-pro` para tarefas complexas (mais caro, mais poderoso)
- O modo `run_debug()` mostra todos os detalhes da execução
- Leia os comentários no código dos exemplos

---

**Pronto para começar? Execute `python google-adk-examples/01_basic_agent.py` agora! 🚀**
