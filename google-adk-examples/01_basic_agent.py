"""
Exemplo 1: Agente Básico com Google ADK
========================================

Este é o exemplo mais simples de um agente usando o Google ADK.
O agente responde a perguntas usando o modelo Gemini.

Para executar:
1. Configure GOOGLE_API_KEY no arquivo .env
2. Execute: python 01_basic_agent.py
"""

import os
import asyncio
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.genai import types

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Verifica se a API Key está configurada
if not os.getenv("GOOGLE_API_KEY"):
    print("❌ Erro: Configure GOOGLE_API_KEY no arquivo .env")
    print("   Obtenha sua chave em: https://aistudio.google.com/app/apikey")
    exit(1)

# Configuração de retry para lidar com erros temporários
retry_config = types.HttpRetryOptions(
    attempts=5,  # Número máximo de tentativas
    exp_base=7,  # Multiplicador de delay
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Códigos HTTP para retry
)


async def main():
    """Função principal que cria e executa o agente."""

    print("🤖 Criando agente básico com Google ADK...\n")

    # Criar o agente
    agent = Agent(
        name="AssistenteBasico",
        model=Gemini(
            model="gemini-2.5-flash-lite",  # Modelo rápido e econômico
            retry_options=retry_config
        ),
        instruction="""Você é um assistente útil e amigável.
        Responda às perguntas de forma clara e concisa."""
    )

    # Criar o runner para executar o agente
    runner = InMemoryRunner(agent=agent)

    # Executar o agente com uma pergunta
    print("📝 Fazendo pergunta ao agente...\n")
    response = await runner.run_debug(
        "Explique em 2-3 frases o que é um agente de IA."
    )

    print("\n✅ Exemplo básico concluído!")


if __name__ == "__main__":
    asyncio.run(main())
