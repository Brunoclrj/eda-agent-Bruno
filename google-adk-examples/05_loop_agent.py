"""
Exemplo 5: Loop Agent - Refinamento Iterativo
==============================================

Este exemplo demonstra um workflow de loop para refinamento iterativo:
1. InitialWriterAgent: Escreve o primeiro rascunho
2. CriticAgent: Avalia e fornece feedback
3. RefinerAgent: Refina baseado no feedback OU sai do loop

O loop continua até que o crítico aprove ou atinja o máximo de iterações.

Para executar:
1. Configure GOOGLE_API_KEY no arquivo .env
2. Execute: python 05_loop_agent.py
"""

import os
import asyncio
from dotenv import load_dotenv
from google.adk.agents import Agent, LoopAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import FunctionTool
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


# ========================================
# Função de Saída do Loop
# ========================================
def exit_loop():
    """Função chamada quando a história é aprovada e o loop deve terminar."""
    return {
        "status": "approved",
        "message": "História aprovada. Saindo do loop de refinamento."
    }


async def main():
    """Função principal que cria e executa o sistema de loop."""

    print("🤖 Criando sistema de refinamento iterativo (loop)...\n")

    # ========================================
    # 1. Agente Escritor Inicial
    # ========================================
    initial_writer_agent = Agent(
        name="InitialWriterAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""Baseado no prompt do usuário, escreva o primeiro rascunho
        de uma história curta (100-150 palavras).
        Retorne apenas o texto da história, sem introdução ou explicação.""",
        output_key="current_story",
    )

    # ========================================
    # 2. Agente Crítico
    # ========================================
    critic_agent = Agent(
        name="CriticAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""Você é um crítico construtivo de histórias.
        Avalie a história fornecida abaixo.

        História: {current_story}

        Avalie o enredo, personagens e ritmo da história.
        - Se a história está bem escrita e completa, você DEVE responder
          com a frase EXATA: "APPROVED"
        - Caso contrário, forneça 2-3 sugestões específicas e práticas
          para melhoria.""",
        output_key="critique",
    )

    # ========================================
    # 3. Agente Refinador
    # ========================================
    refiner_agent = Agent(
        name="RefinerAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""Você é um refinador de histórias.
        Você tem um rascunho e uma crítica.

        Rascunho da História: {current_story}
        Crítica: {critique}

        Sua tarefa é analisar a crítica:
        - SE a crítica for EXATAMENTE "APPROVED", você DEVE chamar a
          função `exit_loop` e nada mais.
        - CASO CONTRÁRIO, reescreva o rascunho da história incorporando
          completamente o feedback da crítica.""",
        output_key="current_story",  # Sobrescreve a história com a versão refinada
        tools=[FunctionTool(exit_loop)],
    )

    # ========================================
    # 4. Estrutura: Sequential + Loop
    # ========================================
    # LoopAgent contém os agentes que executam repetidamente
    story_refinement_loop = LoopAgent(
        name="StoryRefinementLoop",
        sub_agents=[critic_agent, refiner_agent],
        max_iterations=2,  # Previne loops infinitos
    )

    # Root agent: primeiro escreve, depois entra no loop de refinamento
    root_agent = SequentialAgent(
        name="StoryPipeline",
        sub_agents=[initial_writer_agent, story_refinement_loop],
    )

    # ========================================
    # 5. Executar o sistema
    # ========================================
    runner = InMemoryRunner(agent=root_agent)

    print("📝 Escrevendo história sobre 'um faroleiro que descobre um mapa misterioso'...\n")
    print("⏳ Processando:")
    print("   1. Escrever rascunho inicial")
    print("   2. Loop: Criticar → Refinar (até aprovação ou max iterações)")
    print("")

    response = await runner.run_debug(
        "Escreva uma história curta sobre um faroleiro que descobre um mapa misterioso e brilhante"
    )

    print("\n✅ Sistema de loop concluído!")
    print("\n💡 Como funciona o loop:")
    print("   - CriticAgent avalia a história")
    print("   - RefinerAgent melhora OU chama exit_loop() se aprovado")
    print("   - Loop continua até aprovação ou max_iterations")


if __name__ == "__main__":
    asyncio.run(main())
