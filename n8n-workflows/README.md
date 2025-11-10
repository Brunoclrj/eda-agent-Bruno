# 💬 Slack AI Chat - Channel History Q&A

Chat com um canal do Slack usando IA. Este workflow busca o histórico de mensagens do canal e permite fazer perguntas em linguagem natural sobre o conteúdo.

**Características principais:**
- 📊 Analisa até 200 mensagens dos últimos 7 dias
- 🤖 Responde apenas com base em mensagens reais (sem invenções)
- 🔍 Identifica decisões, action items, blockers e questões
- 📝 Gera resumos estruturados
- 🇧🇷 Interface em português

---

## 📋 Índice

- [Requisitos](#-requisitos)
- [Configuração Passo a Passo](#-configuração-passo-a-passo)
- [Como Usar](#-como-usar)
- [Exemplos de Perguntas](#-exemplos-de-perguntas)
- [Estrutura do Workflow](#-estrutura-do-workflow)
- [Customização](#-customização)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Requisitos

- **n8n** instalado e rodando (self-hosted ou cloud)
- **Conta OpenAI** com API key e créditos
- **Workspace Slack** com permissões para criar apps

---

## ⚙️ Configuração Passo a Passo

### 1️⃣ Configurar OpenAI

1. Acesse [OpenAI Platform](https://platform.openai.com)
2. Vá em **Billing** → Adicione créditos à sua conta
3. Vá em **API Keys** → Crie uma nova chave
4. No n8n:
   - Vá em **Credentials** → **New**
   - Selecione **OpenAI**
   - Cole sua API key
   - Salve como "OpenAI account"

### 2️⃣ Configurar Slack App

#### Criar o App no Slack

1. Acesse [Slack API Apps](https://api.slack.com/apps)
2. Clique em **Create New App** → **From scratch**
3. Nome do app: `AI Chat Assistant`
4. Selecione seu workspace

#### Configurar Permissões (Scopes)

1. No menu lateral, vá em **OAuth & Permissions**
2. Role até **Bot Token Scopes**
3. Adicione os seguintes scopes:

   **Permissões para ler mensagens:**
   - `channels:history` - Ler mensagens de canais públicos
   - `channels:read` - Listar canais públicos
   - `groups:history` - Ler mensagens de canais privados
   - `groups:read` - Listar canais privados
   - `im:history` - Ler mensagens diretas
   - `mpim:history` - Ler mensagens de grupos
   - `users:read` - Informações de usuários

   **Opcional (se quiser que o bot responda no Slack):**
   - `chat:write` - Enviar mensagens

#### Instalar o App no Workspace

1. Role para cima na mesma página (**OAuth & Permissions**)
2. Clique em **Install to Workspace**
3. Revise as permissões e autorize
4. **Copie o Bot User OAuth Token** (começa com `xoxb-`)

#### Adicionar o Bot ao Canal

1. No Slack, abra o canal que você quer monitorar
2. Digite `/invite @AI Chat Assistant`
3. O bot precisa estar no canal para ler o histórico

### 3️⃣ Configurar Credenciais no n8n

1. No n8n, vá em **Credentials** → **New**
2. Selecione **Slack OAuth2 API**
3. Configure:
   - **Access Token**: Cole o Bot User OAuth Token do Slack
   - Deixe os outros campos em branco
4. Clique em **Save**
5. Nomeie como "Slack account"

### 4️⃣ Importar o Workflow

1. No n8n, clique em **Add workflow**
2. No menu (três pontos), clique em **Import from File**
3. Selecione o arquivo `slack-ai-chat.json`
4. O workflow será importado

### 5️⃣ Configurar o Workflow

1. Abra o nó **"Slack - Get Channel History"**
2. Em **Credential to connect with**, selecione "Slack account"
3. Em **Channel**, selecione o canal que você quer monitorar
4. Clique em **Save**

5. Verifique o nó **"OpenAI Chat"**:
   - Credential deve estar configurado como "OpenAI account"
   - Model: `gpt-4-turbo-preview` (ou `gpt-4`, `gpt-3.5-turbo`)

6. **Ative o workflow** clicando no toggle no canto superior direito

---

## 🚀 Como Usar

### Método 1: Chat Integrado no n8n

1. Com o workflow ativo, clique em **Chat** no canto superior direito
2. Digite sua pergunta em português
3. Aguarde a análise das mensagens do Slack
4. Receba a resposta baseada no histórico real

### Método 2: Webhook (para integrar com outras ferramentas)

Após ativar o workflow, você receberá uma URL de webhook. Use-a para enviar perguntas via HTTP POST:

```bash
curl -X POST https://seu-n8n.com/webhook/slack-ai-chat \
  -H "Content-Type: application/json" \
  -d '{
    "chatInput": "Quais foram as decisões tomadas ontem?"
  }'
```

---

## 🗣️ Exemplos de Perguntas

### Resumos
- *"Faça um resumo das últimas 24 horas em 5 pontos"*
- *"Resuma as discussões da última sprint planning"*
- *"O que aconteceu na reunião de ontem?"*

### Action Items
- *"Quais action items foram atribuídos e para quem?"*
- *"Liste todas as tarefas mencionadas esta semana"*
- *"Quem ficou responsável por cada tarefa?"*

### Blockers e Problemas
- *"Mostre mensagens com a palavra 'blocker' dos últimos 2 dias"*
- *"Quem está bloqueado e por quê?"*
- *"Quais problemas foram reportados hoje?"*

### Questões e Dúvidas
- *"Liste perguntas que ainda não foram respondidas"*
- *"Quais dúvidas foram levantadas sobre o projeto X?"*

### Análise de Participação
- *"Quem foi mencionado mais vezes esta semana?"*
- *"Quem mais participou das discussões?"*
- *"Liste todos os usuários que comentaram sobre [tema]"*

### Decisões
- *"Quais decisões foram tomadas sobre arquitetura?"*
- *"Resuma as conclusões da última reunião"*
- *"O que foi decidido sobre o prazo do projeto?"*

### Arquivos e Links
- *"Que arquivos foram compartilhados hoje?"*
- *"Liste todos os links enviados esta semana"*
- *"Quais documentos foram mencionados?"*

---

## 🏗️ Estrutura do Workflow

O workflow possui 8 nós principais:

```
┌─────────────────────────┐
│ When chat message       │  Recebe sua pergunta
│ received                │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Slack - Get Channel     │  Busca histórico do canal
│ History                 │  (últimos 7 dias, 200 msgs)
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Process Messages        │  Formata mensagens para IA
│                         │  (usuário, timestamp, texto)
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Check Messages Exist    │  Verifica se há mensagens
└─────┬─────────────┬─────┘
      │ SIM         │ NÃO
      ▼             ▼
┌───────────┐  ┌──────────────┐
│ OpenAI    │  │ Send Error   │
│ Chat      │  │ Message      │
└─────┬─────┘  └──────────────┘
      │
      ▼
┌─────────────────────────┐
│ Format Response         │  Formata resposta com metadados
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Send Response           │  Retorna a resposta
└─────────────────────────┘
```

### Nós Explicados

1. **When chat message received**: Trigger que inicia o workflow quando você envia uma mensagem
2. **Slack - Get Channel History**: Busca as últimas 200 mensagens dos últimos 7 dias do canal configurado
3. **Process Messages**: Formata as mensagens em um formato legível para a IA (timestamp, usuário, texto)
4. **Check Messages Exist**: Valida se há mensagens para analisar
5. **OpenAI Chat**: Envia o contexto e sua pergunta para o GPT-4, com instruções para responder apenas com base nas mensagens
6. **Format Response**: Adiciona metadados à resposta (quantidade de mensagens analisadas)
7. **Send Response**: Retorna a resposta formatada
8. **Send Error Message**: Envia mensagem de erro se não houver mensagens

---

## 🎨 Customização

### Alterar Período de Análise

No nó **"Slack - Get Channel History"**, edite o filtro `oldest`:

```javascript
// Últimos 3 dias
={{ $today.minus({ days: 3 }).toUnixInteger() }}

// Última semana
={{ $today.minus({ days: 7 }).toUnixInteger() }}

// Último mês
={{ $today.minus({ days: 30 }).toUnixInteger() }}

// Período específico (ex: desde 1º de janeiro de 2025)
={{ DateTime.fromISO('2025-01-01').toUnixInteger() }}
```

### Alterar Quantidade de Mensagens

No nó **"Slack - Get Channel History"**:
- Mude **Limit** de `200` para qualquer número entre 1-1000

### Mudar o Modelo da OpenAI

No nó **"OpenAI Chat"**, altere o campo **Model**:
- `gpt-4-turbo-preview` - Mais inteligente, mais caro
- `gpt-4` - Versão estável do GPT-4
- `gpt-3.5-turbo` - Mais rápido e barato

### Ajustar Temperatura da IA

No nó **"OpenAI Chat"** → **Options** → **Temperature**:
- `0.0` - Respostas mais determinísticas e objetivas
- `0.3` - Padrão atual, bom equilíbrio
- `0.7` - Respostas mais criativas
- `1.0` - Máxima criatividade

### Adicionar Filtros de Mensagens

No nó **"Process Messages"**, você pode filtrar mensagens:

```javascript
// Apenas mensagens de um usuário específico
const filteredMessages = messages.filter(msg =>
  msg.json.user === 'U01234567'
);

// Apenas mensagens com uma palavra-chave
const filteredMessages = messages.filter(msg =>
  msg.json.text.toLowerCase().includes('release')
);

// Apenas threads
const filteredMessages = messages.filter(msg =>
  msg.json.thread_ts
);
```

---

## 🔧 Troubleshooting

### ❌ Erro: "Channel not found"

**Causa**: O bot não tem acesso ao canal

**Solução**:
1. No Slack, vá ao canal
2. Digite `/invite @AI Chat Assistant`
3. Confirme que o bot aparece na lista de membros

### ❌ Erro: "missing_scope"

**Causa**: Faltam permissões no Slack App

**Solução**:
1. Vá em [Slack API Apps](https://api.slack.com/apps)
2. Selecione seu app
3. **OAuth & Permissions** → Adicione os scopes necessários
4. **Reinstale o app** no workspace (importante!)
5. Copie o novo token e atualize no n8n

### ❌ Erro: "Invalid Authentication"

**Causa**: Token do Slack incorreto ou expirado

**Solução**:
1. Vá em [Slack API Apps](https://api.slack.com/apps)
2. Selecione seu app
3. **OAuth & Permissions** → Copie o **Bot User OAuth Token**
4. No n8n, edite a credential "Slack account" e atualize o token

### ❌ Erro: "OpenAI API Error: Insufficient funds"

**Causa**: Sem créditos na conta OpenAI

**Solução**:
1. Acesse [OpenAI Billing](https://platform.openai.com/account/billing)
2. Adicione créditos à sua conta (mínimo $5)

### ❌ Não encontra mensagens

**Verificar**:
1. O canal está correto?
2. Há mensagens nos últimos 7 dias?
3. O bot tem permissão de leitura?
4. O filtro de data não está muito restritivo?

**Solução**:
- Execute o workflow em modo de teste
- Clique no nó "Slack - Get Channel History"
- Verifique se retorna dados
- Se estiver vazio, ajuste o período ou o limite

### ❌ Respostas genéricas ou incorretas

**Causa**: IA não está seguindo as instruções ou contexto está confuso

**Solução**:
1. Reduza a temperatura para 0.1-0.2
2. Limite a quantidade de mensagens (100-150)
3. Use um modelo mais avançado (GPT-4)
4. Seja mais específico na pergunta

---

## 📊 Custos Estimados

### OpenAI (GPT-4 Turbo)
- **Input**: $0.01 / 1K tokens
- **Output**: $0.03 / 1K tokens

**Exemplo**: Analisar 200 mensagens + resposta típica
- Input: ~3.000 tokens = $0.03
- Output: ~500 tokens = $0.015
- **Total por consulta**: ~$0.045

**Para reduzir custos**:
- Use `gpt-3.5-turbo` ($0.0005/1K input, $0.0015/1K output)
- Limite o número de mensagens analisadas
- Seja específico nas perguntas para respostas mais curtas

---

## 📝 Notas Importantes

1. **Privacidade**: As mensagens são enviadas para a API da OpenAI. Não use em canais com dados sensíveis ou confidenciais sem revisar os termos de uso da OpenAI.

2. **Limites do Slack API**: O Slack tem rate limits. Se fizer muitas requisições, pode ser bloqueado temporariamente.

3. **Histórico**: O workflow busca apenas mensagens dos últimos X dias (configurável). Mensagens antigas não são incluídas.

4. **Threads**: O workflow lê threads, mas elas são marcadas como `[Thread Reply]` na formatação.

5. **Anexos e Reações**: O workflow atual foca em texto. Anexos, reações e formatação rica não são processados.

---

## 🚀 Próximas Melhorias

Possíveis extensões para o workflow:

- [ ] Salvar histórico de conversas em banco de dados
- [ ] Cache de mensagens para reduzir chamadas ao Slack API
- [ ] Análise de anexos e links
- [ ] Suporte a múltiplos canais em uma única pergunta
- [ ] Integração com Notion/Google Docs para relatórios
- [ ] Alertas automáticos baseados em palavras-chave
- [ ] Dashboard com métricas do canal

---

## 🤝 Contribuições

Encontrou um bug? Tem uma sugestão? Abra uma issue ou pull request!

---

## 📄 Licença

Este workflow é fornecido como está, sem garantias. Use por sua conta e risco.

---

**Desenvolvido para análise inteligente de canais Slack com n8n + OpenAI** 🤖
