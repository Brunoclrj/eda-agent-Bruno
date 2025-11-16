"""
Exemplo 3: Sequential Agent - Pipeline de Criação de Blog
==========================================================

Este exemplo demonstra um workflow sequencial com 3 agentes:
1. OutlineAgent: Cria um esboço do post
2. WriterAgent: Escreve o post completo
3. EditorAgent: Edita e melhora o texto

Os agentes executam em ordem garantida, como uma linha de montagem.

Para executar:
1. Configure GOOGLE_API_KEY no arquivo .env
2. Execute: python 03_sequential_agent.py
"""

import os
import asyncio
from dotenv import load_dotenv
from google.adk.agents import Agent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
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
    """Função principal que cria e executa o pipeline sequencial."""

    print("🤖 Criando pipeline sequencial de blog...\n")

    # ========================================
    # 1. Agente de Esboço
    # ========================================
    outline_agent = Agent(
        name="OutlineAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""Crie um esboço de post de blog para o tópico fornecido com:
        1. Um título chamativo
        2. Uma introdução interessante
        3. 3-5 seções principais com 2-3 pontos cada
        4. Uma conclusão""",
        output_key="blog_outline",
    )

    # ========================================
    # 2. Agente Escritor
    # ========================================
    writer_agent = Agent(
        name="WriterAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""Seguindo este esboço: {blog_outline}

        Escreva um post de blog de 200-300 palavras com tom envolvente e informativo.""",
        output_key="blog_draft",
    )

    # ========================================
    # 3. Agente Editor
    # ========================================
    editor_agent = Agent(
        name="EditorAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""Edite este rascunho: {blog_draft}

        Sua tarefa é:
        - Corrigir erros gramaticais
        - Melhorar o fluxo e estrutura das frases
        - Aumentar a clareza geral do texto""",
        output_key="final_blog",
    )

    # ========================================
    # 4. Pipeline Sequencial (Root Agent)
    # ========================================
    # Os agentes executam na ordem exata que são listados
    root_agent = SequentialAgent(
        name="BlogPipeline",
        sub_agents=[outline_agent, writer_agent, editor_agent],
    )

    # ========================================
    # 5. Executar o pipeline
    # ========================================
    runner = InMemoryRunner(agent=root_agent)

    print("📝 Criando post sobre 'Benefícios de sistemas multi-agente'...\n")
    print("⏳ Processando: Esboço → Escrita → Edição...\n")

    response = await runner.run_debug(
        "Escreva um post de blog sobre os benefícios de sistemas multi-agente para desenvolvedores"
    )

    print("\n✅ Pipeline sequencial concluído!")
    print("\n💡 Note como cada agente processou a saída do anterior:")
    print("   OutlineAgent → blog_outline")
    print("   WriterAgent usa {blog_outline} → blog_draft")
    print("   EditorAgent usa {blog_draft} → final_blog")


if __name__ == "__main__":
    asyncio.run(main())
