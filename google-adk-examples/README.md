# 🚀 Exemplos do Google ADK (Agent Development Kit)

Este diretório contém exemplos práticos para aprender a usar o Google ADK, baseados no curso do Kaggle "5-day Agents Course".

## 📋 Pré-requisitos

1. **Instalar dependências:**
   ```bash
   pip install google-adk google-genai python-dotenv
   ```

2. **Configurar API Key do Google Gemini:**
   - Obtenha sua chave em: https://aistudio.google.com/app/apikey
   - Adicione no arquivo `.env` na raiz do projeto:
     ```
     GOOGLE_API_KEY=sua_chave_aqui
     ```

## 📚 Exemplos Disponíveis

### 1. Agente Básico (`01_basic_agent.py`)
**O que aprende:**
- Criar um agente simples
- Configurar o modelo Gemini
- Executar perguntas básicas

**Execute:**
```bash
python google-adk-examples/01_basic_agent.py
```

---

### 2. Sistema Multi-Agente (`02_multi_agent_research.py`)
**O que aprende:**
- Criar múltiplos agentes especializados
- Usar AgentTool para encapsular agentes
- Coordenar agentes com um agente raiz
- Usar google_search tool

**Agentes:**
- `ResearchAgent`: Busca informações
- `SummarizerAgent`: Resume resultados
- `ResearchCoordinator`: Orquestra o workflow

**Execute:**
```bash
python google-adk-examples/02_multi_agent_research.py
```

---

### 3. Sequential Agent (`03_sequential_agent.py`)
**O que aprende:**
- Criar pipelines com ordem garantida
- Passar dados entre agentes usando `output_key`
- Usar placeholders `{variavel}` nas instruções

**Pipeline:**
```
OutlineAgent → WriterAgent → EditorAgent
   (esboço)      (rascunho)     (final)
```

**Execute:**
```bash
python google-adk-examples/03_sequential_agent.py
```

---

### 4. Parallel Agent (`04_parallel_agent.py`)
**O que aprende:**
- Executar agentes em paralelo para velocidade
- Combinar resultados paralelos com agregador
- Usar SequentialAgent + ParallelAgent juntos

**Estrutura:**
```
┌─────────────────┐
│  Sequential     │
│  ┌───────────┐  │
│  │ Parallel  │  │
│  │  ├─Tech   │  │
│  │  ├─Health │  │  → Aggregator → Resultado
│  │  └─Finance│  │
│  └───────────┘  │
└─────────────────┘
```

**Execute:**
```bash
python google-adk-examples/04_parallel_agent.py
```

---

### 5. Loop Agent (`05_loop_agent.py`)
**O que aprende:**
- Criar workflows iterativos
- Usar FunctionTool para controle de loop
- Implementar refinamento baseado em feedback

**Fluxo:**
```
Escrever → ┌─────────────────────┐
           │ Loop (max 2x):      │
           │  Criticar → Refinar │
           └─────────────────────┘
```

**Execute:**
```bash
python google-adk-examples/05_loop_agent.py
```

---

## 🎯 Escolhendo o Padrão Certo

| Padrão | Quando Usar | Exemplo |
|--------|------------|---------|
| **Agente Básico** | Tarefas simples e diretas | Responder perguntas |
| **Multi-Agente com LLM** | Orquestração dinâmica | Coordenador decide o que fazer |
| **Sequential** | Ordem importa, pipeline linear | Outline → Write → Edit |
| **Parallel** | Tarefas independentes, velocidade | Pesquisar 3 tópicos ao mesmo tempo |
| **Loop** | Refinamento iterativo | Escrever → Criticar → Melhorar |

## 🔑 Conceitos Importantes

### 1. Output Keys
Agentes armazenam resultados no estado da sessão:
```python
Agent(
    name="Writer",
    instruction="...",
    output_key="draft"  # Armazena resultado como 'draft'
)
```

### 2. Placeholders
Outros agentes podem acessar esses valores:
```python
Agent(
    name="Editor",
    instruction="Edit this: {draft}",  # Usa o 'draft' do agente anterior
)
```

### 3. AgentTool
Encapsula agentes como ferramentas:
```python
root_agent = Agent(
    tools=[AgentTool(sub_agent1), AgentTool(sub_agent2)]
)
```

### 4. FunctionTool
Encapsula funções Python como ferramentas:
```python
def my_function():
    return {"result": "success"}

agent = Agent(
    tools=[FunctionTool(my_function)]
)
```

## 📖 Recursos Adicionais

- **Documentação Oficial do ADK**: https://cloud.google.com/vertex-ai/docs/agent-builder
- **Curso Kaggle (5-day Agents)**: https://www.kaggle.com/learn/agents
- **Vídeo do Curso**: https://www.youtube.com/watch?v=ZaUcqznlhv8

## 🛠️ Troubleshooting

### Erro: "GOOGLE_API_KEY não configurada"
- Verifique se o arquivo `.env` existe na raiz do projeto
- Verifique se a variável está correta: `GOOGLE_API_KEY=...`
- Certifique-se de que está usando `load_dotenv()` no código

### Erro 429 (Rate Limit)
- Você atingiu o limite de requisições
- Aguarde alguns segundos e tente novamente
- A configuração `retry_config` já tenta lidar com isso automaticamente

### Erro 500/503/504 (Servidor)
- Erros temporários do servidor Google
- A configuração `retry_config` tenta automaticamente 5 vezes
- Se persistir, aguarde alguns minutos

## 🎓 Próximos Passos

Depois de dominar esses exemplos:
1. Experimente combinar diferentes padrões
2. Crie custom tools personalizadas
3. Explore MCP (Model Context Protocol)
4. Implemente workflows mais complexos

## 📝 Notas

- Todos os exemplos usam `gemini-2.5-flash-lite` (rápido e econômico)
- Você pode trocar por `gemini-2.5-flash` ou `gemini-2.5-pro` conforme necessário
- O modo `run_debug()` mostra detalhes da execução
- Use `run()` para execução silenciosa em produção

---

**Boa sorte aprendendo sobre agentes de IA com o Google ADK! 🚀**
