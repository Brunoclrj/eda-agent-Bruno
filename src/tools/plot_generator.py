"""
Plot Generator - Geração de gráficos analíticos
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Optional
import os


class PlotGenerator:
    """Gerador de gráficos analíticos"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def create_histogram(self, column: str, bins: int = 30) -> go.Figure:
        """Histograma para distribuição"""
        fig = px.histogram(
            self.df,
            x=column,
            nbins=bins,
            title=f'Distribuição de {column}',
            labels={column: column, 'count': 'Frequência'}
        )
        fig.update_layout(
            showlegend=False,
            template='plotly_white',
            height=500
        )
        return fig
    
    def create_boxplot(self, columns: list) -> go.Figure:
        """Boxplot para detectar outliers"""
        fig = go.Figure()
        for col in columns:
            fig.add_trace(go.Box(y=self.df[col], name=col))
        
        fig.update_layout(
            title='Boxplot - Detecção de Outliers',
            yaxis_title='Valor',
            template='plotly_white',
            height=500
        )
        return fig
    
    def create_correlation_heatmap(self, numeric_cols: list) -> go.Figure:
        """Heatmap de correlação"""
        corr_matrix = self.df[numeric_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.index,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 8}
        ))
        
        fig.update_layout(
            title='Matriz de Correlação',
            xaxis_title='Variáveis',
            yaxis_title='Variáveis',
            template='plotly_white',
            height=600,
            width=800
        )
        return fig
    
    def create_scatter(self, x_col: str, y_col: str, color_col: Optional[str] = None) -> go.Figure:
        """Gráfico de dispersão"""
        fig = px.scatter(
            self.df,
            x=x_col,
            y=y_col,
            color=color_col,
            title=f'{y_col} vs {x_col}',
            labels={x_col: x_col, y_col: y_col},
            template='plotly_white',
            height=500
        )
        return fig
    
    def create_time_series(self, time_col: str, value_col: str) -> go.Figure:
        """Série temporal"""
        df_sorted = self.df[[time_col, value_col]].dropna().sort_values(time_col)
        
        fig = px.line(
            df_sorted,
            x=time_col,
            y=value_col,
            title=f'Evolução Temporal de {value_col}',
            labels={time_col: 'Tempo', value_col: value_col},
            template='plotly_white',
            height=500
        )
        return fig
    
    def save_figure(self, fig: go.Figure, filename: str, output_dir: str = './outputs') -> str:
        """Salva figura como PNG"""
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        fig.write_image(filepath, width=800, height=600)
        return filepath
