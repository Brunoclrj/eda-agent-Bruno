"""
Exemplo 4: Parallel Agent - Pesquisa Multi-Tópico
==================================================

Este exemplo demonstra execução paralela de agentes independentes:
- TechResearcher: Pesquisa tendências de tecnologia
- HealthResearcher: Pesquisa avanços médicos
- FinanceResearcher: Pesquisa tendências financeiras
- AggregatorAgent: Combina todos os resultados

Os 3 pesquisadores executam simultaneamente (em paralelo) para velocidade,
depois o agregador combina os resultados.

Para executar:
1. Configure GOOGLE_API_KEY no arquivo .env
2. Execute: python 04_parallel_agent.py
"""

import os
import asyncio
from dotenv import load_dotenv
from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
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
    """Função principal que cria e executa o sistema paralelo."""

    print("🤖 Criando sistema de pesquisa paralela...\n")

    # ========================================
    # 1. Agente de Pesquisa - Tecnologia
    # ========================================
    tech_researcher = Agent(
        name="TechResearcher",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""Pesquise as últimas tendências em IA/ML.
        Inclua 3 desenvolvimentos principais, empresas envolvidas e impacto potencial.
        Mantenha o relatório conciso (100 palavras).""",
        tools=[google_search],
        output_key="tech_research",
    )

    # ========================================
    # 2. Agente de Pesquisa - Saúde
    # ========================================
    health_researcher = Agent(
        name="HealthResearcher",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""Pesquise avanços médicos recentes.
        Inclua 3 avanços significativos, aplicações práticas e cronogramas.
        Mantenha o relatório conciso (100 palavras).""",
        tools=[google_search],
        output_key="health_research",
    )

    # ========================================
    # 3. Agente de Pesquisa - Finanças
    # ========================================
    finance_researcher = Agent(
        name="FinanceResearcher",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""Pesquise tendências atuais em fintech.
        Inclua 3 tendências principais, implicações de mercado e perspectivas.
        Mantenha o relatório conciso (100 palavras).""",
        tools=[google_search],
        output_key="finance_research",
    )

    # ========================================
    # 4. Agente Agregador
    # ========================================
    aggregator_agent = Agent(
        name="AggregatorAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""Combine estas três pesquisas em um resumo executivo:

        **Tendências Tecnológicas:**
        {tech_research}

        **Avanços em Saúde:**
        {health_research}

        **Inovações Financeiras:**
        {finance_research}

        Seu resumo deve destacar temas comuns, conexões surpreendentes
        e as principais conclusões de todos os três relatórios.
        Resumo final: aproximadamente 200 palavras.""",
        output_key="executive_summary",
    )

    # ========================================
    # 5. Estrutura: Paralelo + Sequencial
    # ========================================
    # ParallelAgent executa todos os pesquisadores SIMULTANEAMENTE
    parallel_research_team = ParallelAgent(
        name="ParallelResearchTeam",
        sub_agents=[tech_researcher, health_researcher, finance_researcher],
    )

    # SequentialAgent define o fluxo: primeiro paralelo, depois agregador
    root_agent = SequentialAgent(
        name="ResearchSystem",
        sub_agents=[parallel_research_team, aggregator_agent],
    )

    # ========================================
    # 6. Executar o sistema
    # ========================================
    runner = InMemoryRunner(agent=root_agent)

    print("📝 Executando briefing executivo diário em Tech, Saúde e Finanças...\n")
    print("⏳ Os 3 pesquisadores estão trabalhando em PARALELO...")
    print("   Isso é muito mais rápido do que executar sequencialmente!\n")

    response = await runner.run_debug(
        "Execute o briefing executivo diário sobre Tech, Saúde e Finanças"
    )

    print("\n✅ Sistema paralelo concluído!")
    print("\n💡 Benefício do paralelismo:")
    print("   - 3 pesquisas independentes executam ao mesmo tempo")
    print("   - Tempo total ≈ tempo de 1 pesquisa (não 3x)")
    print("   - Agregador executa após todas completarem")


if __name__ == "__main__":
    asyncio.run(main())
