@echo off
REM Script de instalação do Google ADK para Windows
REM Execute: google-adk-examples\setup.bat

echo 🚀 Instalando Google ADK para desenvolvimento...
echo.

REM Verificar se está na raiz do projeto
if not exist ".env.example" (
    echo ❌ Erro: Execute este script na raiz do projeto eda-agent-Bruno
    exit /b 1
)

REM 1. Criar ambiente virtual
echo 📦 1/4 - Criando ambiente virtual...
if exist "venv-adk" (
    echo    ⚠️  venv-adk já existe, pulando...
) else (
    python -m venv venv-adk
    echo    ✅ Ambiente virtual criado
)

REM 2. Ativar ambiente virtual e instalar dependências
echo.
echo 📥 2/4 - Instalando dependências do Google ADK...
call venv-adk\Scripts\activate.bat
python -m pip install --upgrade pip >nul 2>&1
pip install -r google-adk-examples\requirements-adk.txt
echo    ✅ Dependências instaladas

REM 3. Configurar .env
echo.
echo 🔑 3/4 - Configurando arquivo .env...
if exist ".env" (
    echo    ⚠️  Arquivo .env já existe
    echo    Verifique se GOOGLE_API_KEY está configurada
) else (
    copy .env.example .env >nul
    echo    ✅ Arquivo .env criado
    echo    ⚠️  IMPORTANTE: Edite o arquivo .env e adicione sua GOOGLE_API_KEY
    echo    Obtenha em: https://aistudio.google.com/app/apikey
)

REM 4. Verificar instalação
echo.
echo 🧪 4/4 - Verificando instalação...
python -c "import google.adk; import google.genai; print('   ✅ Importações OK')" 2>nul

echo.
echo ✨ Instalação concluída!
echo.
echo 📝 Próximos passos:
echo    1. Ative o ambiente virtual:
echo       venv-adk\Scripts\activate
echo.
echo    2. Configure sua API Key no arquivo .env:
echo       GOOGLE_API_KEY=sua_chave_aqui
echo.
echo    3. Execute o primeiro exemplo:
echo       python google-adk-examples\01_basic_agent.py
echo.
echo 📚 Documentação completa em: google-adk-examples\QUICKSTART.md

pause
