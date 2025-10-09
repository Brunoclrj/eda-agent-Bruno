"""
Gerador de Relatório PDF - 7 Itens Obrigatórios
"""
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
from typing import List, Tuple
import os


class PDFReportGenerator:
    """Gerador do relatório PDF da atividade"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configura estilos personalizados"""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Title'],
            fontSize=20,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=1  # Center
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading1'],
            fontSize=14,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=20
        )
    
    def generate_report(
        self,
        framework: str,
        architecture_description: str,
        questions_answers: List[Tuple[str, str, str]],  # (question, answer, plot_path)
        conclusions_qa: Tuple[str, str],  # (question, answer)
        source_code_info: str,
        public_link: str,
        output_path: str = "Agentes Autônomos – Relatório da Atividade Extra.pdf"
    ):
        """
        Gera o relatório PDF com os 7 itens obrigatórios
        
        Args:
            framework: Nome do framework/plataforma utilizado
            architecture_description: Descrição da arquitetura
            questions_answers: Lista de (pergunta, resposta, caminho_do_grafico)
            conclusions_qa: Tupla (pergunta_sobre_conclusoes, resposta)
            source_code_info: Informação sobre onde encontrar o código
            public_link: Link público para acessar o agente
            output_path: Caminho do arquivo PDF de saída
        """
        
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Título principal
        story.append(Paragraph(
            "Agentes Autônomos<br/>Relatório da Atividade Extra",
            self.title_style
        ))
        story.append(Spacer(1, 0.2*inch))
        
        # Informações gerais
        info_data = [
            ['Data:', datetime.now().strftime('%d/%m/%Y')],
            ['Aluno:', '[Seu Nome]'],
            ['Curso:', 'Agentes Autônomos com IA Generativa - I²A²']
        ]
        info_table = Table(info_data, colWidths=[1.5*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#555555')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.5*inch))
        
        # 1. Framework/Plataforma
        story.append(Paragraph("1. Framework/Plataforma Escolhida", self.heading_style))
        story.append(Paragraph(framework, self.styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # 2. Arquitetura
        story.append(Paragraph("2. Como a Solução Foi Estruturada", self.heading_style))
        story.append(Paragraph(architecture_description, self.styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # 3. Perguntas e Respostas (≥4, ≥1 com gráfico)
        story.append(PageBreak())
        story.append(Paragraph(
            f"3. Perguntas e Respostas ({len(questions_answers)} perguntas testadas)",
            self.heading_style
        ))
        
        for i, (question, answer, plot_path) in enumerate(questions_answers, 1):
            # Pergunta
            question_style = ParagraphStyle(
                'Question',
                parent=self.styles['Normal'],
                fontSize=11,
                textColor=colors.HexColor('#2c3e50'),
                fontName='Helvetica-Bold',
                spaceBefore=15
            )
            story.append(Paragraph(f"<b>Pergunta {i}:</b> {question}", question_style))
            story.append(Spacer(1, 0.1*inch))
            
            # Resposta
            story.append(Paragraph(f"<b>Resposta:</b>", self.styles['Normal']))
            story.append(Paragraph(answer, self.styles['Normal']))
            
            # Gráfico (se houver)
            if plot_path and os.path.exists(plot_path):
                story.append(Spacer(1, 0.2*inch))
                story.append(Paragraph("<i>Gráfico gerado pelo agente:</i>", self.styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
                
                try:
                    img = Image(plot_path, width=5*inch, height=3.5*inch)
                    story.append(img)
                except Exception as e:
                    story.append(Paragraph(
                        f"<i>[Erro ao carregar gráfico: {e}]</i>",
                        self.styles['Normal']
                    ))
            
            story.append(Spacer(1, 0.3*inch))
        
        # 4. Pergunta sobre Conclusões
        story.append(PageBreak())
        story.append(Paragraph("4. Pergunta sobre as Conclusões do Agente", self.heading_style))
        story.append(Paragraph(f"<b>Pergunta:</b> {conclusions_qa[0]}", self.styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph(f"<b>Resposta do Agente:</b>", self.styles['Normal']))
        story.append(Paragraph(conclusions_qa[1], self.styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # 5. Códigos Fonte
        story.append(Paragraph("5. Códigos Fonte / Arquivo JSON de Exportação", self.heading_style))
        story.append(Paragraph(source_code_info, self.styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
        
        code_note = """
        <b>Nota importante:</b> Todas as chaves de API foram removidas do código-fonte 
        conforme item 7 (Ocultação de Chaves). O código utiliza variáveis de ambiente 
        para gerenciar secrets de forma segura.
        """
        story.append(Paragraph(code_note, self.styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # 6. Link Público
        story.append(Paragraph("6. Link para Acessar o Agente", self.heading_style))
        story.append(Paragraph(
            f'<b>URL de acesso público:</b> <a href="{public_link}" color="blue">{public_link}</a>',
            self.styles['Normal']
        ))
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph(
            "<i>Através deste link, é possível testar o agente com qualquer arquivo CSV.</i>",
            self.styles['Normal']
        ))
        story.append(Spacer(1, 0.3*inch))
        
        # 7. Ocultação de Chaves
        story.append(Paragraph("7. Ocultação de Chaves Utilizadas nos Artefatos", self.heading_style))
        
        security_measures = """
        <b>Medidas de segurança implementadas:</b><br/>
        <br/>
        ✓ <b>Variáveis de ambiente:</b> Todas as chaves de API são carregadas via arquivo .env<br/>
        ✓ <b>Arquivo .gitignore:</b> O arquivo .env está listado no .gitignore para não ser versionado<br/>
        ✓ <b>Template .env.example:</b> Fornecido como referência, sem chaves reais<br/>
        ✓ <b>Secrets do Streamlit Cloud:</b> Configuração via interface do Streamlit Cloud<br/>
        ✓ <b>Código limpo:</b> Nenhuma chave hardcoded no código-fonte<br/>
        <br/>
        <i>Evidência:</i> Consulte o arquivo .gitignore e .env.example no repositório, 
        e verifique que o código-fonte não contém strings de API keys.
        """
        story.append(Paragraph(security_measures, self.styles['Normal']))
        
        # Build PDF
        doc.build(story)
        print(f"✅ Relatório PDF gerado com sucesso: {output_path}")
        
        return output_path


# Exemplo de uso
if __name__ == "__main__":
    generator = PDFReportGenerator()
    
    # Dados de exemplo para o relatório
    generator.generate_report(
        framework="""
        <b>Framework:</b> Claude Sonnet 4.5 (Anthropic) + Streamlit<br/>
        <br/>
        A solução utiliza o modelo de linguagem Claude Sonnet 4.5 para processar 
        perguntas em linguagem natural e executar análises exploratórias de dados. 
        A interface é construída em Streamlit, permitindo interação intuitiva via 
        navegador web. O sistema de memória usa ChromaDB para busca semântica e 
        SQLite para armazenamento estruturado de conclusões.
        """,
        
        architecture_description="""
        A arquitetura é composta por 5 componentes principais:<br/>
        <br/>
        1. <b>CSV Handler:</b> Detecta automaticamente encoding e delimitador, normaliza 
           colunas e gera metadata completo do dataset<br/>
        2. <b>EDA Engine:</b> Executa análises estatísticas (distribuição, outliers, 
           correlação, tendências temporais, clustering)<br/>
        3. <b>Plot Generator:</b> Cria visualizações usando Plotly (histogramas, 
           boxplots, heatmaps, scatter plots, séries temporais)<br/>
        4. <b>Memory Store:</b> Armazena análises e conclusões usando ChromaDB (busca 
           semântica) e SQLite (queries estruturadas)<br/>
        5. <b>EDA Agent:</b> Orquestra todo o fluxo, interpretando perguntas, decidindo 
           ferramentas e sintetizando respostas<br/>
        <br/>
        O agente segue o padrão ReAct (Raciocínio + Ação), planejando análises antes 
        de executá-las e armazenando conclusões na memória para contexto futuro.
        """,
        
        questions_answers=[
            (
                "Descreva a distribuição da coluna Amount",
                "A coluna Amount apresenta distribuição assimétrica (skewness positivo), "
                "com concentração de valores baixos e alguns outliers significativos. "
                "Média: $88.35, Mediana: $22.00, indicando presença de transações de "
                "alto valor que elevam a média.",
                "./outputs/histogram_amount.png"
            ),
            (
                "Mostre um heatmap de correlação entre as variáveis",
                "O heatmap revela correlações fracas entre a maioria das variáveis V1-V28 "
                "(resultado esperado do PCA). A correlação mais forte observada é entre "
                "V2 e V5 (0.65). Amount não apresenta correlação significativa com as "
                "componentes PCA.",
                "./outputs/correlation_heatmap.png"
            ),
            (
                "Existem outliers na coluna Amount?",
                "Sim, detectados 1.081 outliers (0.38% dos dados) usando método IQR. "
                "Limites: Q1=$5.60, Q3=$77.17, IQR=$71.57. Outliers incluem transações "
                "acima de $184.83. Recomenda-se investigar se representam fraudes ou "
                "comportamento legítimo.",
                None
            ),
            (
                "Há tendência temporal na coluna Time?",
                "Análise temporal de Time vs Amount mostra padrão cíclico sem tendência "
                "linear clara (R²=0.002). Observa-se variação de atividade ao longo do "
                "período de 48h, possivelmente relacionado a horários comerciais.",
                "./outputs/timeseries_time.png"
            ),
        ],
        
        conclusions_qa=(
            "Quais as principais conclusões sobre este dataset?",
            "Com base nas análises realizadas:\n\n"
            "1. O dataset possui forte desbalanceamento de classes (fraudes são raras)\n"
            "2. As variáveis V1-V28 (PCA) têm baixa correlação entre si, conforme esperado\n"
            "3. Transações fraudulentas tendem a ter valores mais baixos que as normais\n"
            "4. Existem outliers significativos que merecem investigação detalhada\n"
            "5. Padrões temporais sugerem variação de atividade por horário\n\n"
            "Recomendações: usar técnicas de balanceamento de classes, investigar outliers "
            "individualmente e considerar features temporais em modelos preditivos."
        ),
        
        source_code_info="""
        O código-fonte completo está organizado em módulos Python:<br/>
        <br/>
        • <b>src/agent/eda_agent.py</b> - Agente principal (ReAct)<br/>
        • <b>src/tools/csv_handler.py</b> - Processamento de CSV<br/>
        • <b>src/tools/eda_engine.py</b> - Análises estatísticas<br/>
        • <b>src/tools/plot_generator.py</b> - Geração de gráficos<br/>
        • <b>src/memory/memory_store.py</b> - Sistema de memória<br/>
        • <b>src/ui/app.py</b> - Interface Streamlit<br/>
        <br/>
        Todos os arquivos estão anexados a este e-mail e disponíveis no repositório GitHub.
        """,
        
        public_link="https://seu-app-eda.streamlit.app"
    )
