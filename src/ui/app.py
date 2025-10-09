"""
Aplicação Streamlit - Interface para o Agente EDA
"""
import streamlit as st
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from agent.eda_agent import EDAAgent
from tools.csv_handler import CSVHandler
from tools.eda_engine import EDAEngine
from tools.plot_generator import PlotGenerator
from memory.memory_store import MemoryStore

# Configuração da página
st.set_page_config(
    page_title="Agente EDA Autônomo",
    page_icon="📊",
    layout="wide"
)

# Inicializar estado da sessão
if 'csv_handler' not in st.session_state:
    st.session_state.csv_handler = None
if 'dataset_hash' not in st.session_state:
    st.session_state.dataset_hash = None
if 'memory' not in st.session_state:
    st.session_state.memory = MemoryStore()
if 'agent' not in st.session_state:
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        st.error("⚠️ ANTHROPIC_API_KEY não configurada! Configure no arquivo .env")
        st.stop()
    st.session_state.agent = EDAAgent(api_key)

# Título
st.title("🤖 Agente Autônomo para Análise Exploratória de Dados")
st.markdown("### Faça perguntas sobre qualquer CSV em linguagem natural")

# Sidebar para upload
with st.sidebar:
    st.header("1️⃣ Carregar Dataset")
    
    uploaded_file = st.file_uploader(
        "Upload arquivo CSV",
        type=['csv'],
        help="Qualquer CSV com qualquer delimitador/encoding"
    )
    
    sample_size = st.number_input(
        "Linhas para amostragem (0 = todas)",
        min_value=0,
        max_value=1000000,
        value=10000,
        step=1000
    )
    
    if uploaded_file and st.button("🔄 Carregar CSV", type="primary"):
        with st.spinner("Carregando e processando CSV..."):
            # Salvar temporariamente
            temp_dir = "./data/uploads"
            os.makedirs(temp_dir, exist_ok=True)
            temp_path = os.path.join(temp_dir, uploaded_file.name)
            
            with open(temp_path, 'wb') as f:
                f.write(uploaded_file.getvalue())
            
            # Processar
            csv_handler = CSVHandler()
            csv_handler.load_csv(temp_path, sample_size)
            
            st.session_state.csv_handler = csv_handler
            st.session_state.dataset_hash = st.session_state.memory.register_dataset(
                temp_path,
                csv_handler.metadata
            )
            
            st.success(f"✅ CSV carregado: {csv_handler.metadata['shape']}")
            st.rerun()
    
    # Mostrar metadata se carregado
    if st.session_state.csv_handler:
        st.divider()
        st.subheader("📋 Metadata do Dataset")
        
        meta = st.session_state.csv_handler.metadata
        st.metric("Linhas", meta['shape'][0])
        st.metric("Colunas", meta['shape'][1])
        
        with st.expander("Ver colunas"):
            st.write("**Numéricas:**", meta['column_types']['numeric'][:10])
            st.write("**Categóricas:**", meta['column_types']['categorical'][:5])

# Área principal
if st.session_state.csv_handler:
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["💬 Fazer Perguntas", "🧠 Memória & Conclusões", "📊 Amostra dos Dados"])
    
    with tab1:
        st.subheader("Faça sua pergunta sobre os dados")
        
        # Exemplos
        with st.expander("💡 Exemplos de perguntas"):
            st.markdown("""
            - "Descreva a distribuição de todas as variáveis numéricas"
            - "Mostre um heatmap de correlação entre as variáveis"
            - "Existem outliers na coluna Amount? Mostre um boxplot"
            - "Há tendência temporal na coluna Time?"
            - "Faça uma análise de clusters nos dados numéricos"
            """)
        
        question = st.text_input(
            "Sua pergunta:",
            placeholder="Ex: Qual a distribuição da coluna Class? Mostre um gráfico.",
            key="question_input"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            ask_button = st.button("🚀 Perguntar", type="primary", use_container_width=True)
        
        if ask_button and question:
            with st.spinner("🤖 Agente analisando..."):
                
                # Preparar componentes
                eda_engine = EDAEngine(
                    st.session_state.csv_handler.df,
                    st.session_state.csv_handler.metadata
                )
                
                plot_generator = PlotGenerator(st.session_state.csv_handler.df)
                
                # Processar pergunta
                result = st.session_state.agent.process_question(
                    question=question,
                    csv_handler=st.session_state.csv_handler,
                    eda_engine=eda_engine,
                    plot_generator=plot_generator,
                    memory=st.session_state.memory,
                    dataset_hash=st.session_state.dataset_hash
                )
                
                # Exibir resposta
                st.markdown("### 📝 Resposta do Agente")
                st.markdown(result['answer'])
                
                # Exibir gráfico se houver
                if result['plot_fig']:
                    st.markdown("### 📊 Visualização")
                    st.plotly_chart(result['plot_fig'], use_container_width=True)
                
                # Mostrar conclusões
                with st.expander("🎯 Conclusões armazenadas na memória"):
                    st.info(result['conclusions'])
    
    with tab2:
        st.subheader("🧠 Histórico de Conclusões")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🔄 Atualizar"):
                st.rerun()
        
        conclusions = st.session_state.memory.get_conclusions(
            st.session_state.dataset_hash,
            limit=20
        )
        
        if conclusions:
            st.success(f"📚 {len(conclusions)} análises encontradas")
            
            for i, conc in enumerate(conclusions, 1):
                with st.expander(f"{i}. {conc['question'][:80]}... • {conc['timestamp'][:10]}"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**Tipo:** `{conc['analysis_type']}`")
                    with col2:
                        if conc['has_plot']:
                            st.badge("📊 Com gráfico", type="success")
                    
                    st.markdown("**Conclusão:**")
                    st.write(conc['conclusions'])
        else:
            st.info("💡 Nenhuma conclusão ainda. Faça perguntas na aba 'Fazer Perguntas' para começar!")
        
        # Pergunta sobre conclusões
        st.divider()
        st.subheader("🔍 Pergunte sobre as Conclusões Acumuladas")
        
        conclusion_question = st.text_input(
            "Ex: Quais as principais conclusões até agora sobre este dataset?",
            key="conclusion_q"
        )
        
        if st.button("💬 Perguntar sobre conclusões"):
            if not conclusion_question:
                st.warning("Digite uma pergunta primeiro!")
            else:
                with st.spinner("Consultando memória..."):
                    answer = st.session_state.agent.answer_about_conclusions(
                        question=conclusion_question,
                        memory=st.session_state.memory,
                        dataset_hash=st.session_state.dataset_hash
                    )
                    
                    st.markdown("### 💡 Síntese das Conclusões")
                    st.markdown(answer)
    
    with tab3:
        st.subheader("📊 Amostra dos Dados")
        
        n_rows = st.slider("Número de linhas", 5, 100, 10)
        st.dataframe(
            st.session_state.csv_handler.df.head(n_rows),
            use_container_width=True
        )
        
        st.divider()
        st.subheader("📈 Estatísticas Descritivas")
        st.dataframe(
            st.session_state.csv_handler.df.describe(),
            use_container_width=True
        )

else:
    # Tela inicial
    st.info("👈 **Carregue um CSV na barra lateral para começar**")
    
    st.markdown("""
    ## 🎯 Como usar este agente:
    
    1. **Carregue um CSV** na barra lateral
    2. **Faça perguntas** em linguagem natural sobre os dados
    3. **Visualize gráficos** gerados automaticamente
    4. **Consulte conclusões** acumuladas pelo agente
    
    ### Exemplos de perguntas que você pode fazer:
    
    - "Descreva a distribuição de todas as variáveis e destaque outliers"
    - "Mostre correlações entre colunas numéricas (heatmap)"
    - "Existe tendência temporal? Mostre um gráfico de série"
    - "Quais as principais conclusões sobre este dataset?"
    - "Faça uma análise de clusters e identifique padrões"
    
    ---
    
    ### ⚙️ Tecnologias utilizadas:
    - **LLM:** Claude Sonnet 4.5 (Anthropic)
    - **Interface:** Streamlit
    - **Processamento:** Pandas, NumPy, SciPy
    - **Visualização:** Plotly
    - **Memória:** ChromaDB + SQLite
    """)
    
    # Avisos
    col1, col2 = st.columns(2)
    with col1:
        st.warning("⚠️ Certifique-se de ter configurado ANTHROPIC_API_KEY no arquivo .env")
    with col2:
        st.info("ℹ️ O agente suporta qualquer CSV com qualquer formato/encoding")

# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🔗 Link público: [Será gerado após deploy]")
with col2:
    st.caption("📚 Atividade: Agentes Autônomos - I²A²")
with col3:
    st.caption("🤖 Powered by Claude Sonnet 4.5")
