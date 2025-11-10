# 🏗️ Arquitetura do Workflow - Slack AI Chat

Documentação técnica detalhada do workflow para desenvolvedores.

---

## 📊 Visão Geral

O workflow implementa um padrão de **RAG (Retrieval-Augmented Generation)** simples:

```
Usuário → Trigger → Busca Dados → Processa → IA → Formata → Responde
```

**Fluxo de Dados:**
1. **Entrada**: Pergunta do usuário
2. **Contexto**: Mensagens do Slack (últimos N dias)
3. **Processamento**: Formatação e validação
4. **IA**: Análise com OpenAI GPT
5. **Saída**: Resposta estruturada

---

## 🧩 Componentes do Workflow

### 1. Chat Trigger Node

**ID**: `a1b2c3d4-e5f6-7890-abcd-ef1234567890`
**Tipo**: `n8n-nodes-base.chatTrigger`

**Função**: Ponto de entrada do workflow

**Output Schema**:
```json
{
  "chatInput": "string",     // Pergunta do usuário
  "sessionId": "string",     // ID da sessão
  "action": "string"         // Tipo de ação
}
```

**Configuração**:
- `webhookId`: Identificador único para o webhook
- Expõe uma interface de chat integrada no n8n

---

### 2. Slack History Node

**ID**: `b2c3d4e5-f6a7-8901-bcde-f12345678901`
**Tipo**: `n8n-nodes-base.slack`

**Função**: Buscar mensagens do canal

**Parâmetros Principais**:
```javascript
{
  resource: "message",
  operation: "getAll",
  channelId: "C01234567",       // ID do canal
  returnAll: false,
  limit: 200,                    // Máximo de mensagens
  filters: {
    oldest: "{{ $today.minus({ days: 7 }).toUnixInteger() }}"
  }
}
```

**Output Schema** (por mensagem):
```json
{
  "ts": "1234567890.123456",    // Timestamp único
  "user": "U01234567",          // User ID
  "text": "Mensagem...",        // Conteúdo
  "type": "message",
  "channel": "C01234567",
  "thread_ts": "...",           // Se for thread
  "reactions": [...],           // Array de reações
  "files": [...]                // Anexos
}
```

**Limitações da API Slack**:
- Máximo: 1000 mensagens por request
- Rate limit: ~1 req/segundo (Tier 3)
- Não inclui mensagens deletadas
- Threads são items separados

---

### 3. Process Messages Node

**ID**: `c3d4e5f6-a7b8-9012-cdef-123456789012`
**Tipo**: `n8n-nodes-base.code`

**Função**: Transformar mensagens em contexto legível

**Código Completo**:
```javascript
// Process Slack messages into a readable format for AI
const messages = $input.all();

// Format messages with timestamp, user, and text
const formattedMessages = messages.map(msg => {
  const item = msg.json;

  // Convert Unix timestamp to readable date
  const timestamp = new Date(parseFloat(item.ts) * 1000)
    .toLocaleString('pt-BR');

  // Get user info
  const user = item.user || item.username || 'Unknown';

  // Get message text
  const text = item.text || '';

  // Mark thread replies
  const threadInfo = item.thread_ts ? ` [Thread Reply]` : '';

  return `[${timestamp}] ${user}${threadInfo}: ${text}`;
});

// Join all messages into a single context
const context = formattedMessages.join('\n\n');

// Get the user's question
const userQuestion = $('When chat message received').item.json.chatInput;

return {
  context: context,
  question: userQuestion,
  messageCount: messages.length,
  channelId: messages[0]?.json.channel || 'unknown'
};
```

**Output Schema**:
```json
{
  "context": "string",        // Todas as mensagens formatadas
  "question": "string",       // Pergunta do usuário
  "messageCount": 123,        // Quantidade de mensagens
  "channelId": "C01234567"    // ID do canal
}
```

**Transformação Exemplo**:
```
Input (Slack):
{
  "ts": "1704067200.123456",
  "user": "U01234567",
  "text": "Precisamos resolver o bug #123"
}

Output (Formatado):
"[01/01/2024 10:00:00] U01234567: Precisamos resolver o bug #123"
```

---

### 4. Check Messages Exist Node

**ID**: `g7h8i9j0-e1f2-3456-a123-567890123456`
**Tipo**: `n8n-nodes-base.if`

**Função**: Validar se há mensagens para processar

**Lógica**:
```javascript
// Condição
if (context !== "" && context !== null && context !== undefined) {
  return true;  // Output: True (continua para OpenAI)
} else {
  return false; // Output: False (vai para erro)
}
```

**Rotas**:
- **True** → OpenAI Chat
- **False** → Send Error Message

---

### 5. OpenAI Chat Node

**ID**: `d4e5f6a7-b8c9-0123-def1-234567890123`
**Tipo**: `n8n-nodes-base.openAi`

**Função**: Processar pergunta com contexto usando IA

**Configuração Completa**:
```javascript
{
  operation: "message",
  model: "gpt-4-turbo-preview",
  messages: [
    {
      role: "system",
      message: `Você é um assistente especializado em analisar históricos de conversas do Slack.

      REGRAS IMPORTANTES:
      1. Responda APENAS com base nas mensagens fornecidas
      2. Se a informação não estiver nas mensagens, diga claramente
      3. Cite mensagens específicas quando relevante
      4. Seja objetivo e direto
      5. Para resumos, organize em bullet points
      6. Identifique action items, decisões, blockers e questões quando solicitado

      CONTEXTO - HISTÓRICO DO CANAL ({{ $json.messageCount }} mensagens):

      {{ $json.context }}`
    },
    {
      role: "user",
      message: "{{ $json.question }}"
    }
  ],
  options: {
    temperature: 0.3,     // Baixa = mais determinístico
    maxTokens: 2000       // Limite de resposta
  }
}
```

**Sistema de Prompt**:

1. **Identity**: Define o papel da IA
2. **Rules**: Regras estritas para evitar alucinações
3. **Context**: Injeta todas as mensagens formatadas
4. **User Query**: A pergunta específica

**Output Schema**:
```json
{
  "message": {
    "role": "assistant",
    "content": "Resposta da IA..."
  },
  "usage": {
    "prompt_tokens": 1234,
    "completion_tokens": 567,
    "total_tokens": 1801
  }
}
```

---

### 6. Format Response Node

**ID**: `e5f6a7b8-c9d0-1234-ef12-345678901234`
**Tipo**: `n8n-nodes-base.code`

**Função**: Adicionar metadados à resposta

**Código**:
```javascript
// Extract AI response
const aiResponse = $input.first().json.message.content;

// Get metadata from previous node
const messageCount = $('Process Messages').first().json.messageCount;
const channelId = $('Process Messages').first().json.channelId;

return {
  chatResponse: aiResponse,
  metadata: {
    messagesAnalyzed: messageCount,
    channelId: channelId,
    timestamp: new Date().toISOString()
  }
};
```

**Output Schema**:
```json
{
  "chatResponse": "string",
  "metadata": {
    "messagesAnalyzed": 123,
    "channelId": "C01234567",
    "timestamp": "2025-01-10T12:00:00.000Z"
  }
}
```

---

### 7. Send Response Node

**ID**: `f6a7b8c9-d0e1-2345-f123-456789012345`
**Tipo**: `n8n-nodes-base.respondToWebhook`

**Função**: Retornar resposta ao usuário

**Configuração**:
```javascript
{
  respondWith: "text",
  responseBody: `{{ $json.chatResponse }}

---
_Analisadas {{ $json.metadata.messagesAnalyzed }} mensagens do canal_`
}
```

**Formato Final**:
```
[Resposta da IA aqui...]

---
_Analisadas 147 mensagens do canal_
```

---

### 8. Send Error Message Node

**ID**: `h8i9j0k1-f2a3-4567-b123-678901234567`
**Tipo**: `n8n-nodes-base.respondToWebhook`

**Função**: Informar erros ao usuário

**Mensagem Padrão**:
```
Não encontrei mensagens no canal especificado. Verifique se:
1. O canal ID está correto
2. O bot tem permissões para ler o histórico
3. Existem mensagens nos últimos 7 dias
```

---

## 🔄 Fluxo de Dados Detalhado

### Cenário: Usuário pergunta "Quais foram os blockers?"

#### Step 1: Trigger Recebe Input
```json
{
  "chatInput": "Quais foram os blockers?",
  "sessionId": "abc123"
}
```

#### Step 2: Slack Busca Mensagens
```json
[
  {
    "ts": "1704067200.123456",
    "user": "U123",
    "text": "Estou bloqueado no bug #456"
  },
  {
    "ts": "1704067260.789012",
    "user": "U456",
    "text": "Consegui resolver o blocker"
  }
  // ... mais 148 mensagens
]
```

#### Step 3: Processa e Formata
```json
{
  "context": "[01/01/2024 10:00] U123: Estou bloqueado no bug #456\n\n[01/01/2024 10:01] U456: Consegui resolver o blocker",
  "question": "Quais foram os blockers?",
  "messageCount": 150
}
```

#### Step 4: OpenAI Analisa
```
System: [Instruções + Contexto completo]
User: Quais foram os blockers?

AI Response:
"Identifiquei 1 blocker mencionado:

1. Bug #456 (U123, 01/01 10:00)
   - Status: Resolvido
   - Resolução: U456 resolveu às 10:01

Não há blockers ativos no momento."
```

#### Step 5: Formata e Responde
```
Identifiquei 1 blocker mencionado:
[...]

---
_Analisadas 150 mensagens do canal_
```

---

## 🔐 Segurança

### Dados Sensíveis

**⚠️ IMPORTANTE**: As mensagens são enviadas para a API OpenAI

**Dados Transmitidos**:
- Conteúdo completo das mensagens
- Usernames/IDs
- Timestamps
- Conteúdo de threads

**Não é Transmitido**:
- Arquivos anexados (apenas mencionados)
- Reações
- Mensagens deletadas

**Recomendações**:
1. Revise os [Termos de Uso da OpenAI](https://openai.com/policies/terms-of-use)
2. Não use em canais com dados sensíveis/confidenciais
3. Implemente autenticação no webhook (veja `.env.example`)
4. Use variáveis de ambiente para credenciais

---

## ⚡ Performance

### Tempo de Execução Típico

| Etapa | Tempo | Notas |
|-------|-------|-------|
| Trigger | ~10ms | Instantâneo |
| Slack API | 500-2000ms | Depende da quantidade de mensagens |
| Processamento | 50-200ms | Depende da quantidade |
| OpenAI API | 3000-8000ms | GPT-4 é mais lento que 3.5 |
| Formatação | ~50ms | Instantâneo |
| **TOTAL** | **4-10s** | Para 200 mensagens |

### Otimizações Possíveis

**1. Cache de Mensagens**
```javascript
// Armazenar mensagens em banco de dados
// Buscar apenas novas mensagens (> last_ts)
// Reduz chamadas ao Slack API
```

**2. Usar GPT-3.5-turbo**
```javascript
// 10x mais rápido
// 20x mais barato
// Menos preciso em análises complexas
```

**3. Limitar Tokens**
```javascript
// Resumir mensagens antigas
// Manter apenas últimas 100 mensagens completas
// Reduz custo da OpenAI
```

---

## 🧪 Testing

### Teste Manual

1. Execute o workflow em modo de teste
2. Clique em cada nó após execução
3. Verifique os outputs

### Casos de Teste

**Caso 1: Canal Vazio**
- Input: Pergunta qualquer
- Expected: Mensagem de erro "Não encontrei mensagens"

**Caso 2: Pergunta Específica**
- Input: "Quem mencionou 'deploy'?"
- Expected: Resposta citando mensagens específicas

**Caso 3: Resumo Geral**
- Input: "Resuma as últimas 24h"
- Expected: Lista de bullet points

**Caso 4: Informação Não Presente**
- Input: "Quem está de férias?"
- Expected: "Não encontrei essa informação nas mensagens"

---

## 🔧 Extensões Futuras

### 1. Multi-Channel Support
```javascript
// Permitir análise de múltiplos canais
channels: ["channel1", "channel2", "channel3"]
```

### 2. Busca Vetorial
```javascript
// Usar embeddings para busca semântica
// Pinecone/Weaviate para armazenar vetores
// Buscar apenas mensagens relevantes
```

### 3. Histórico de Conversas
```javascript
// Armazenar contexto entre perguntas
// Permitir follow-up questions
// "Me fale mais sobre o segundo item"
```

### 4. Análise de Threads
```javascript
// Expandir threads automaticamente
// Agrupar mensagens relacionadas
// Mostrar hierarquia de respostas
```

### 5. Alertas Automáticos
```javascript
// Trigger agendado (cron)
// Analisar mensagens a cada 1h
// Enviar alerta se detectar blocker/problema
```

---

## 📚 Referências

- [n8n Nodes Documentation](https://docs.n8n.io/integrations/)
- [Slack API - conversations.history](https://api.slack.com/methods/conversations.history)
- [OpenAI Chat API](https://platform.openai.com/docs/api-reference/chat)
- [RAG (Retrieval-Augmented Generation)](https://arxiv.org/abs/2005.11401)

---

## 🤝 Contribuindo

Se você fez melhorias ou correções:

1. Documente as mudanças
2. Atualize este arquivo
3. Adicione testes
4. Abra um PR

---

**Desenvolvido com n8n, Slack API e OpenAI** 🛠️
