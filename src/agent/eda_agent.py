"""
EDA Agent - Agente para Análise Exploratória de Dados
Versão simplificada sem LangGraph (pode ser implementado depois)
"""
from anthropic import Anthropic
import json
import os
from typing import Dict, Any, Optional
import sys

# Adicionar diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tools.csv_handler import CSVHandler
from tools.eda_engine import EDAEngine
from tools.plot_generator import PlotGenerator
from memory.memory_store import MemoryStore


class EDAAgent:
    """Agente de EDA com raciocínio ReAct"""
    
    def __init__(self, anthropic_api_key: str):
        self.client = Anthropic(api_key=anthropic_api_key)
        self.model = "claude-sonnet-4-5-20250929"
    
    def process_question(
        self,
        question: str,
        csv_handler: CSVHandler,
        eda_engine: EDAEngine,
        plot_generator: PlotGenerator,
        memory: MemoryStore,
        dataset_hash: str,
        max_iterations: int = 3
    ) -> Dict[str, Any]:
        """Processa uma pergunta sobre o dataset"""
        
        # Buscar contexto na memória
        similar_analyses = memory.search_similar_analyses(
            query=question,
            dataset_hash=dataset_hash,
            n_results=3
        )
        
        memory_context = "\n".join([
            f"- {a['metadata']['question']}: {a['document'][:150]}..."
            for a in similar_analyses
        ]) if similar_analyses else "Nenhuma análise anterior."
        
        # Prompt principal
        system_prompt = f"""Você é um especialista em Análise Exploratória de Dados (EDA).

Dataset atual:
- Forma: {csv_handler.metadata['shape']}
- Colunas numéricas: {', '.join(eda_engine.numeric_cols[:10])}
- Colunas categóricas: {', '.join(eda_engine.categorical_cols[:5])}

Análises anteriores:
{memory_context}

Você tem acesso às seguintes ferramentas:
1. describe_data - Descreve estrutura do dataset
2. analyze_distribution(column) - Analisa distribuição de uma coluna
3. detect_outliers(column, method='iqr') - Detecta outliers
4. correlation_analysis() - Matriz de correlação
5. temporal_analysis(time_col, value_col) - Análise temporal
6. cluster_analysis(n_clusters=3) - Clustering
7. create_plot(type, params) - Gera gráfico (histogram, boxplot, heatmap, scatter, timeseries)

Responda em 3 etapas:
1. RACIOCÍNIO: Pense sobre qual ferramenta usar
2. AÇÃO: Execute a ferramenta (responda em JSON)
3. RESPOSTA: Sintetize a análise para o usuário

Seja direto, técnico e claro."""

        user_message = f"Pergunta: {question}\n\nSua análise completa:"
        
        # Chamar Claude
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            temperature=0,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )
        
        response_text = response.content[0].text
        
        # Tentar extrair ação JSON
        action_result = None
        plot_fig = None
        
        try:
            # Procurar por JSON na resposta
            import re
            json_match = re.search(r'\{[^{}]*"(action|type)"[^{}]*\}', response_text, re.DOTALL)
            
            if json_match:
                action_dict = json.loads(json_match.group())
                action_result = self._execute_action(
                    action_dict,
                    eda_engine,
                    plot_generator
                )
                
                # Se gerou plot, capturar
                if 'plot_fig' in action_result:
                    plot_fig = action_result.pop('plot_fig')
        except Exception as e:
            action_result = {"info": "Análise conceitual sem execução de ferramenta"}
        
        # Gerar conclusões
        conclusions = self._extract_conclusions(response_text)
        
        # Armazenar na memória
        memory.store_analysis(
            dataset_hash=dataset_hash,
            question=question,
            analysis_type=action_dict.get('action', 'general') if 'action_dict' in locals() else 'general',
            results=action_result or {},
            conclusions=conclusions,
            has_plot=(plot_fig is not None)
        )
        
        return {
            'answer': response_text,
            'conclusions': conclusions,
            'plot_fig': plot_fig,
            'action_result': action_result
        }
    
    def _execute_action(
        self,
        action_dict: Dict,
        eda_engine: EDAEngine,
        plot_generator: PlotGenerator
    ) -> Dict[str, Any]:
        """Executa ação solicitada"""
        
        action = action_dict.get('action') or action_dict.get('type')
        params = action_dict.get('params', {})
        
        try:
            if action == 'describe_data':
                return eda_engine.describe_data()
            
            elif action == 'analyze_distribution':
                return eda_engine.analyze_distribution(params['column'])
            
            elif action == 'detect_outliers':
                return eda_engine.detect_outliers(
                    params['column'],
                    params.get('method', 'iqr')
                )
            
            elif action == 'correlation_analysis':
                return eda_engine.correlation_analysis()
            
            elif action == 'temporal_analysis':
                return eda_engine.temporal_analysis(
                    params['time_col'],
                    params['value_col']
                )
            
            elif action == 'cluster_analysis':
                return eda_engine.cluster_analysis(params.get('n_clusters', 3))
            
            elif action in ['histogram', 'boxplot', 'heatmap', 'scatter', 'timeseries']:
                if action == 'histogram':
                    fig = plot_generator.create_histogram(params['column'])
                elif action == 'boxplot':
                    fig = plot_generator.create_boxplot(params['columns'])
                elif action == 'heatmap':
                    fig = plot_generator.create_correlation_heatmap(
                        eda_engine.numeric_cols[:20]
                    )
                elif action == 'scatter':
                    fig = plot_generator.create_scatter(
                        params['x_col'],
                        params['y_col'],
                        params.get('color_col')
                    )
                elif action == 'timeseries':
                    fig = plot_generator.create_time_series(
                        params['time_col'],
                        params['value_col']
                    )
                
                return {'status': 'Plot gerado', 'plot_fig': fig}
            
            else:
                return {'error': f'Ação desconhecida: {action}'}
        
        except Exception as e:
            return {'error': str(e)}
    
    def _extract_conclusions(self, response_text: str) -> str:
        """Extrai conclusões principais da resposta"""
        # Pegar primeiras frases conclusivas
        lines = response_text.split('\n')
        conclusions = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['conclusão', 'concluir', 'resultado', 'principal', 'importante']):
                conclusions.append(line.strip())
        
        if conclusions:
            return ' '.join(conclusions[:3])
        else:
            # Fallback: últimas frases
            return ' '.join(lines[-3:]) if len(lines) >= 3 else response_text[:300]
    
    def answer_about_conclusions(
        self,
        question: str,
        memory: MemoryStore,
        dataset_hash: str
    ) -> str:
        """Responde perguntas sobre conclusões acumuladas"""
        
        # Buscar conclusões relevantes
        similar = memory.search_similar_analyses(
            query=question,
            dataset_hash=dataset_hash,
            n_results=10
        )
        
        context = "\n\n".join([f"- {s['document']}" for s in similar])
        
        if not context:
            return "Ainda não há conclusões acumuladas para este dataset. Faça algumas perguntas primeiro!"
        
        # Sintetizar com Claude
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            temperature=0,
            system="Você sintetiza conclusões de análises de dados de forma clara e objetiva.",
            messages=[{
                "role": "user",
                "content": f"Conclusões disponíveis:\n{context}\n\nPergunta: {question}\n\nSua resposta:"
            }]
        )
        
        return response.content[0].text
