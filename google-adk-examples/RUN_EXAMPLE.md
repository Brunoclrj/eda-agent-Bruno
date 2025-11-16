# 🎯 Como executar os exemplos no Cursor

## 🖥️ No Cursor (Windows, Mac ou Linux)

### Passo 1: Abrir o Terminal Integrado

1. Abra o projeto `eda-agent-Bruno` no Cursor
2. Abra o terminal integrado: `Ctrl + '` (ou `Cmd + '` no Mac)
3. Certifique-se de estar na raiz do projeto

### Passo 2: Executar o script de instalação

**No Windows:**
```bash
google-adk-examples\setup.bat
```

**No Linux/Mac:**
```bash
bash google-adk-examples/setup.sh
```

### Passo 3: Obter sua API Key do Google

1. Acesse: https://aistudio.google.com/app/apikey
2. Faça login com sua conta Google
3. Clique em **"Create API Key"**
4. Copie a chave (formato: `AIzaSy...`)

### Passo 4: Configurar a API Key

1. Abra o arquivo `.env` no Cursor
2. Encontre a linha: `GOOGLE_API_KEY=sua_chave_google_aqui`
3. Substitua por sua chave real: `GOOGLE_API_KEY=AIzaSy...`
4. Salve o arquivo (`Ctrl+S`)

### Passo 5: Ativar o ambiente virtual

**No Windows:**
```bash
venv-adk\Scripts\activate
```

**No Linux/Mac:**
```bash
source venv-adk/bin/activate
```

Você verá `(venv-adk)` no início da linha do terminal.

### Passo 6: Executar o primeiro exemplo

```bash
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

## 🎮 Executar outros exemplos

Com o ambiente virtual ativado, execute qualquer exemplo:

```bash
# Multi-Agente
python google-adk-examples/02_multi_agent_research.py

# Sequential
python google-adk-examples/03_sequential_agent.py

# Parallel
python google-adk-examples/04_parallel_agent.py

# Loop
python google-adk-examples/05_loop_agent.py
```

## 💡 Dicas para o Cursor

### 1. Usar a IA do Cursor para modificar exemplos

Você pode pedir ao Cursor AI:
- "Modifique o exemplo 01 para perguntar sobre Python"
- "Crie um novo agente que analisa código"
- "Adapte o exemplo 03 para criar um README"

### 2. Debug no Cursor

1. Coloque breakpoints clicando na margem esquerda
2. Pressione `F5` para iniciar debug
3. Use `F10` para step over, `F11` para step into

### 3. Terminal integrado sempre visível

- Configure: `View > Terminal` (ou `Ctrl + '`)
- Mantenha aberto para ver saídas dos agentes

### 4. Git integrado

O Cursor tem controle Git visual:
- `Ctrl+Shift+G` para abrir painel Git
- Veja mudanças, commits, etc.

## 🐛 Problemas comuns

### ❌ "python não é reconhecido"

**Solução:**
- Instale Python: https://www.python.org/downloads/
- Marque "Add Python to PATH" durante instalação
- Reinicie o Cursor

### ❌ "venv-adk não ativou"

**Solução no Windows:**
```bash
# Permitir execução de scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Depois ative novamente
venv-adk\Scripts\activate
```

### ❌ "No module named 'google.adk'"

**Solução:**
```bash
# Certifique-se que o ambiente virtual está ativo
# Você deve ver (venv-adk) no terminal

# Reinstale
pip install -r google-adk-examples/requirements-adk.txt
```

### ❌ "GOOGLE_API_KEY não configurada"

**Solução:**
- Verifique se o arquivo `.env` existe
- Verifique se tem a linha: `GOOGLE_API_KEY=AIza...`
- Sem espaços, sem aspas

## 🚀 Workflow recomendado no Cursor

```bash
# 1. Abrir projeto
cd eda-agent-Bruno

# 2. Ativar ambiente (sempre que abrir novo terminal)
source venv-adk/bin/activate  # ou venv-adk\Scripts\activate no Windows

# 3. Executar ou modificar exemplos
python google-adk-examples/01_basic_agent.py

# 4. Criar seus próprios agentes
# Use o Cursor AI para ajudar!
```

## 📚 Próximos passos

1. ✅ Execute todos os 5 exemplos
2. ✅ Modifique os exemplos com suas próprias perguntas
3. ✅ Crie um agente personalizado para seu projeto EDA
4. ✅ Assista ao curso completo: https://www.youtube.com/watch?v=ZaUcqznlhv8

---

**Dúvidas? Peça ajuda ao Claude Code ou à IA do Cursor! 🤖**
