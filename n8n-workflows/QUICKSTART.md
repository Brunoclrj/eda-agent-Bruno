# ⚡ Quick Start - Slack AI Chat

Guia rápido para colocar o workflow funcionando em menos de 10 minutos.

---

## 📋 Checklist Rápido

- [ ] n8n instalado e rodando
- [ ] Conta OpenAI com créditos
- [ ] Acesso admin ao Slack workspace
- [ ] 10 minutos livres

---

## 🚀 5 Passos Para Começar

### 1. OpenAI (2 min)

```bash
# Vá em: https://platform.openai.com/api-keys
# 1. Clique em "Create new secret key"
# 2. Copie a chave (começa com sk-...)
# 3. No n8n: Credentials → New → OpenAI → Cole a chave → Save
```

✅ **Checkpoint**: Você tem uma credencial "OpenAI account" no n8n

---

### 2. Criar Slack App (3 min)

```bash
# Vá em: https://api.slack.com/apps
# 1. "Create New App" → "From scratch"
# 2. Nome: "AI Chat Assistant"
# 3. Escolha seu workspace
```

✅ **Checkpoint**: Você tem um novo app criado

---

### 3. Configurar Permissões (2 min)

No seu app:
1. Menu lateral → **OAuth & Permissions**
2. Role até **Bot Token Scopes**
3. Clique em **Add an OAuth Scope** e adicione:

```
channels:history
channels:read
groups:history
users:read
```

4. Role para cima e clique em **Install to Workspace**
5. **Copie o Bot User OAuth Token** (xoxb-...)

✅ **Checkpoint**: Você tem um token xoxb-...

---

### 4. Configurar n8n (2 min)

No n8n:
1. **Credentials** → **New** → **Slack OAuth2 API**
2. Cole o token no campo **Access Token**
3. Salve como "Slack account"
4. **Workflows** → **Import from File** → Selecione `slack-ai-chat.json`

No workflow importado:
1. Abra o nó **"Slack - Get Channel History"**
2. Selecione a credencial "Slack account"
3. Selecione o **Canal** que você quer monitorar
4. Save

✅ **Checkpoint**: Workflow importado e configurado

---

### 5. Adicionar Bot ao Canal (1 min)

No Slack:
1. Vá ao canal que você quer monitorar
2. Digite: `/invite @AI Chat Assistant`
3. Confirme

✅ **Checkpoint**: Bot está no canal

---

## 🎉 Pronto! Teste Agora

1. No n8n, **ative o workflow** (toggle no canto superior direito)
2. Clique em **Chat** (ícone de balão)
3. Digite: **"Faça um resumo das últimas 24 horas"**
4. Aguarde a resposta

---

## 🐛 Não Funcionou?

### Erro: "Channel not found"
```bash
# Solução: Bot não está no canal
# No Slack: /invite @AI Chat Assistant
```

### Erro: "missing_scope"
```bash
# Solução: Falta permissão
# Slack API → Seu App → OAuth & Permissions
# Adicione os scopes necessários → Reinstale o app
```

### Erro: "Invalid Authentication"
```bash
# Solução: Token errado
# Copie o token novamente do Slack API
# Atualize a credencial no n8n
```

### Erro: OpenAI
```bash
# Solução: Sem créditos ou chave inválida
# Verifique: https://platform.openai.com/account/billing
# Adicione créditos ($5 mínimo)
```

---

## 📝 Perguntas de Teste

Experimente estas perguntas:

```
✅ Resumos
"Faça um resumo das últimas 24 horas em 5 pontos"

✅ Action Items
"Quais tarefas foram atribuídas e para quem?"

✅ Blockers
"Alguém mencionou algum bloqueio?"

✅ Decisões
"Quais decisões foram tomadas sobre [tema]?"

✅ Participação
"Quem foi mais mencionado nas discussões?"
```

---

## 🎯 Próximos Passos

Agora que está funcionando:

1. 📖 Leia o [README completo](README.md) para customizações
2. 🎨 Ajuste o período de análise (padrão: 7 dias)
3. 🔧 Teste diferentes modelos OpenAI
4. 📊 Explore [exemplos de perguntas](example-questions.json)

---

## 💡 Dicas Rápidas

### Economizar Créditos OpenAI
```javascript
// No nó OpenAI Chat, mude o modelo para:
"gpt-3.5-turbo"  // ~10x mais barato que GPT-4
```

### Analisar Menos Mensagens
```javascript
// No nó Slack, reduza o Limit para:
50  // Apenas últimas 50 mensagens
```

### Respostas Mais Objetivas
```javascript
// No nó OpenAI Chat → Options → Temperature:
0.1  // Mais determinístico
```

---

## 🆘 Precisa de Ajuda?

- 📖 Consulte o [README completo](README.md)
- 🔍 Veja exemplos em [example-questions.json](example-questions.json)
- 🐛 Verifique a seção [Troubleshooting](README.md#-troubleshooting)
- 💬 Abra uma issue no repositório

---

**Tempo estimado**: ⏱️ 10 minutos
**Dificuldade**: 🟢 Fácil
**Custo**: 💰 ~$0.05 por consulta (GPT-4)

---

**Boa análise! 🚀**
