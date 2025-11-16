"""
Exemplo 2: Sistema Multi-Agente - Pesquisa e Resumo
====================================================

Este exemplo demonstra um sistema com dois agentes especializados:
- ResearchAgent: Busca informações usando Google Search
- SummarizerAgent: Cria resumos concisos

Para executar:
1. Configure GOOGLE_API_KEY no arquivo .env
2. Execute: python 02_multi_agent_research.py
"""

import os
import asyncio
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, google_search
from google.genai import types

# Carrega variáveis de ambiente
load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    print("❌ Erro: Configure GOOGLE_API_KEY no arquivo .env")
    exit(1)

# Configuração de retry
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


async def main():
    """Função principal que cria e executa o sistema multi-agente."""

    print("🤖 Criando sistema multi-agente (Pesquisa + Resumo)...\n")

    # ========================================
    # 1. Agente de Pesquisa
    # ========================================
    research_agent = Agent(
        name="ResearchAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""Você é um agente especializado em pesquisa.
        Use a ferramenta google_search para encontrar 2-3 informações relevantes
        sobre o tópico solicitado e apresente os resultados com citações.""",
        tools=[google_search],
        output_key="research_findings",  # Armazena resultado no estado da sessão
    )

    # ========================================
    # 2. Agente de Resumo
    # ========================================
    summarizer_agent = Agent(
        name="SummarizerAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""Leia os resultados da pesquisa: {research_findings}

        Crie um resumo conciso em formato de lista com 3-5 pontos principais.""",
        output_key="final_summary",
    )

    # ========================================
    # 3. Agente Coordenador (Root)
    # ========================================
    root_agent = Agent(
        name="ResearchCoordinator",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""Você é um coordenador de pesquisa.

        Para responder à pergunta do usuário:
        1. PRIMEIRO, chame a ferramenta ResearchAgent para buscar informações
        2. DEPOIS, chame a ferramenta SummarizerAgent para criar um resumo
        3. FINALMENTE, apresente o resumo final ao usuário""",
        # Os sub-agentes são encapsulados como ferramentas
        tools=[AgentTool(research_agent), AgentTool(summarizer_agent)],
    )

    # ========================================
    # 4. Executar o sistema
    # ========================================
    runner = InMemoryRunner(agent=root_agent)

    print("📝 Pesquisando sobre 'Agentes de IA e suas aplicações'...\n")
    print("⏳ Isso pode levar alguns segundos...\n")

    response = await runner.run_debug(
        "Quais são as principais aplicações de agentes de IA atualmente?"
    )

    print("\n✅ Sistema multi-agente concluído!")


if __name__ == "__main__":
    asyncio.run(main())
