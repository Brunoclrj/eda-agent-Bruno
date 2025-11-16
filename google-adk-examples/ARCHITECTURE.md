# 🏗️ Arquitetura - Como tudo funciona

## 🌐 Fluxo completo: Você → Claude Code → GitHub → Cursor

```
┌─────────────────────────────────────────────────────────────┐
│                    SEU WORKFLOW                             │
└─────────────────────────────────────────────────────────────┘

1️⃣ VOCÊ PEDE ALGO AO CLAUDE CODE
   ┌──────────────┐
   │   Você       │  "Configure o Google ADK"
   └──────┬───────┘
          │
          ▼
   ┌──────────────────────┐
   │  Claude Code         │  <- Onde EU estou
   │  (Container Linux)   │     executando agora
   └──────┬───────────────┘
          │
          ├─ Executa comandos (pip install, git, etc)
          ├─ Cria arquivos (.py, .md, etc)
          ├─ Faz commits
          │
          ▼
   ┌──────────────────────┐
   │    GitHub            │
   │  (seu repositório)   │
   └──────┬───────────────┘
          │
          │  git pull/sync
          │
          ▼
   ┌──────────────────────┐
   │   Cursor no seu PC   │  <- Aqui você desenvolve
   │   (VSCode fork)      │
   └──────────────────────┘


2️⃣ VOCÊ DESENVOLVE NO CURSOR
   ┌──────────────────────┐
   │   Cursor (seu PC)    │
   └──────┬───────────────┘
          │
          ├─ Você edita código
          ├─ Executa scripts Python
          ├─ Testa exemplos do ADK
          │
          ▼
   ┌──────────────────────┐
   │  Terminal Cursor     │
   │  venv-adk ativado    │
   │  python examples.py  │
   └──────┬───────────────┘
          │
          │  Quando pronto
          │
          ▼
   ┌──────────────────────┐
   │    GitHub            │  git push
   │  (seu repositório)   │
   └──────────────────────┘
```

## 🔍 Detalhando cada componente

### 1. Claude Code (Container Remoto)

**O que é:**
- Um ambiente Linux isolado e temporário
- Onde EU (Claude Code) executo comandos
- Tem acesso ao seu repositório Git
- É destruído quando nossa conversa termina

**O que posso fazer:**
- ✅ Executar comandos shell (bash, pip, git, etc)
- ✅ Criar e editar arquivos
- ✅ Instalar pacotes Python
- ✅ Fazer commits e push para GitHub
- ❌ Não tenho acesso ao seu PC local
- ❌ Não posso executar GUI ou aplicações interativas

**Por que é temporário:**
```
Conversa inicia → Container criado → Eu trabalho → Conversa termina → Container destruído
                                         ↓
                                    git commit + push
                                         ↓
                                  Mudanças persistem no GitHub!
```

### 2. GitHub (Repositório Central)

**Papel:**
- Armazena todo o código permanentemente
- Sincroniza entre Claude Code e seu Cursor
- Versionamento e histórico

**Branches:**
```
main (ou master)
  ↓
claude/setup-google-adk-01UCpATGGLs4nXQKA5CeviZj  ← Branch que criei
```

### 3. Cursor (Seu ambiente local)

**O que é:**
- Editor de código baseado no VSCode
- Tem IA integrada (similar a GitHub Copilot)
- Roda no SEU computador

**Como conecta com GitHub:**
```bash
# No terminal do Cursor:
git pull origin claude/setup-google-adk-01UCpATGGLs4nXQKA5CeviZj

# Agora você tem os arquivos que eu criei!
```

## 🔄 Ciclo de desenvolvimento completo

```
╔══════════════════════════════════════════════════════════╗
║  FASE 1: Claude Code cria a estrutura inicial            ║
╚══════════════════════════════════════════════════════════╝

Claude Code (container)
  ├─ pip install google-adk
  ├─ Cria exemplos 01-05.py
  ├─ Cria documentação
  ├─ git commit -m "Setup ADK"
  └─ git push
         │
         ▼
    GitHub recebe as mudanças


╔══════════════════════════════════════════════════════════╗
║  FASE 2: Você trabalha no Cursor                         ║
╚══════════════════════════════════════════════════════════╝

Cursor no seu PC
  ├─ git pull (baixa as mudanças)
  ├─ bash setup.sh (instala localmente)
  ├─ Ativa venv-adk
  ├─ python 01_basic_agent.py (executa!)
  ├─ Modifica exemplos
  ├─ Cria seus próprios agentes
  ├─ git commit -m "Meus agentes"
  └─ git push
         │
         ▼
    GitHub recebe SUAS mudanças


╔══════════════════════════════════════════════════════════╗
║  FASE 3: Ciclo contínua (você + Claude Code)             ║
╚══════════════════════════════════════════════════════════╝

Você pede ajuda ao Claude Code
    │
    ▼
Claude Code puxa suas mudanças do GitHub
    │
    ▼
Claude Code faz modificações
    │
    ▼
Claude Code faz push para GitHub
    │
    ▼
Você puxa no Cursor
    │
    ▼
Você continua desenvolvendo
    │
    └─── (ciclo se repete)
```

## 📦 Ambientes Python

### Container do Claude Code:
```
/home/user/eda-agent-Bruno/
  ├─ google-adk instalado globalmente (pip install)
  └─ SEM ambiente virtual (não precisa, é temporário)
```

### Seu PC (Cursor):
```
C:\Users\Você\eda-agent-Bruno\  (Windows)
/home/voce/eda-agent-Bruno/      (Linux)
  ├─ venv-adk/  ← Ambiente virtual (você cria)
  │   └─ google-adk instalado aqui
  └─ google-adk-examples/
      └─ *.py (executam usando venv-adk)
```

## 🎯 Por que usar ambiente virtual no seu PC?

**Isolamento:**
```
Seu PC:
  ├─ Python global (sistema)
  ├─ Projeto A (venv-projeto-a)
  │   └─ google-adk 1.18.0
  ├─ Projeto B (venv-projeto-b)
  │   └─ tensorflow 2.x
  └─ eda-agent-Bruno (venv-adk)
      └─ google-adk + suas dependências
```

Cada projeto tem suas próprias versões, sem conflitos!

## 🔐 Como o GitHub conecta tudo?

```
Claude Code ←──── GitHub ────→ Cursor (seu PC)
                    ▲
                    │
                    │ Autenticação
                    │ (suas credenciais)
                    │
              Seu repositório
              Brunoclrj/eda-agent-Bruno
```

**Autenticação:**
- Você já configurou as credenciais Git no Cursor
- Quando faço `git push`, uso as permissões do repositório
- É como se eu fosse um "colaborador temporário"

## 🎬 Exemplo prático completo

```bash
# 1. EU (Claude Code) crio os exemplos
[Container Linux]
$ pip install google-adk
$ # ... cria arquivos ...
$ git commit -m "Setup ADK"
$ git push origin claude/setup-google-adk-01UCpATGGLs4nXQKA5CeviZj

# 2. VOCÊ no Cursor puxa as mudanças
[Cursor - Terminal]
$ git pull origin claude/setup-google-adk-01UCpATGGLs4nXQKA5CeviZj

# 3. VOCÊ instala localmente
$ bash google-adk-examples/setup.sh
$ source venv-adk/bin/activate

# 4. VOCÊ executa
(venv-adk) $ python google-adk-examples/01_basic_agent.py
🤖 Criando agente básico...
✅ Funcionou!

# 5. VOCÊ modifica e commita
$ git add meu_agente.py
$ git commit -m "Criei meu primeiro agente"
$ git push

# 6. SE você pedir mais ajuda, EU posso ver suas mudanças!
[Claude Code]
$ git pull  # Vejo seu meu_agente.py
$ # ... posso ajudar a melhorar ...
```

## 🤝 Colaboração perfeita

```
┌─────────────────┐         ┌──────────────────┐
│  Claude Code    │         │   Você (Cursor)  │
│                 │         │                  │
│ • Setup inicial │         │ • Desenvolvimento│
│ • Criar exemplos│←─Git──→│ • Testes locais  │
│ • Ajudar debug  │         │ • Customização   │
│ • Documentação  │         │ • Seus agentes   │
└─────────────────┘         └──────────────────┘
         ↓                           ↓
         └────────GitHub─────────────┘
              (sincronização)
```

---

**Resumo:** Eu crio e ajudo no container remoto, você desenvolve no seu PC com Cursor, e o GitHub mantém tudo sincronizado! 🚀
