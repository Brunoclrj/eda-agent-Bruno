"""
EDA Engine - Motor de Análise Exploratória de Dados
"""
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Any


class EDAEngine:
    """Motor de análise exploratória de dados"""
    
    def __init__(self, df: pd.DataFrame, metadata: Dict):
        self.df = df
        self.metadata = metadata
        self.numeric_cols = metadata['column_types']['numeric']
        self.categorical_cols = metadata['column_types']['categorical']
    
    def describe_data(self) -> Dict[str, Any]:
        """Descrição completa dos dados"""
        return {
            'shape': f"{self.df.shape[0]} linhas × {self.df.shape[1]} colunas",
            'types': self.metadata['dtypes'],
            'missing_values': {k: v for k, v in self.metadata['missing'].items() if v > 0},
            'numeric_summary': self.metadata.get('numeric_stats', {}),
            'sample': self.df.head(5).to_dict('records')
        }
    
    def analyze_distribution(self, column: str) -> Dict[str, Any]:
        """Analisa distribuição de uma coluna"""
        if column not in self.df.columns:
            return {'error': f'Coluna {column} não encontrada'}
        
        col_data = self.df[column].dropna()
        
        if pd.api.types.is_numeric_dtype(col_data):
            return {
                'type': 'numeric',
                'count': int(len(col_data)),
                'mean': float(col_data.mean()),
                'median': float(col_data.median()),
                'std': float(col_data.std()),
                'min': float(col_data.min()),
                'max': float(col_data.max()),
                'q25': float(col_data.quantile(0.25)),
                'q75': float(col_data.quantile(0.75)),
                'skewness': float(stats.skew(col_data)),
                'kurtosis': float(stats.kurtosis(col_data))
            }
        else:
            value_counts = col_data.value_counts()
            return {
                'type': 'categorical',
                'unique_values': int(col_data.nunique()),
                'most_common': value_counts.head(10).to_dict(),
                'mode': str(value_counts.index[0]) if len(value_counts) > 0 else None
            }
    
    def detect_outliers(self, column: str, method: str = 'iqr') -> Dict[str, Any]:
        """Detecta outliers em coluna numérica"""
        if column not in self.numeric_cols:
            return {'error': f'{column} não é numérica'}
        
        col_data = self.df[column].dropna()
        
        if method == 'iqr':
            Q1 = col_data.quantile(0.25)
            Q3 = col_data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
        else:  # z-score
            z_scores = np.abs(stats.zscore(col_data))
            outliers = col_data[z_scores > 3]
            lower_bound = None
            upper_bound = None
        
        return {
            'method': method,
            'total_outliers': int(len(outliers)),
            'percentage': f"{len(outliers)/len(col_data)*100:.2f}%",
            'outlier_values': outliers.head(20).tolist(),
            'bounds': {
                'lower': float(lower_bound) if lower_bound is not None else None,
                'upper': float(upper_bound) if upper_bound is not None else None
            }
        }
    
    def correlation_analysis(self) -> Dict[str, Any]:
        """Análise de correlação entre variáveis numéricas"""
        if len(self.numeric_cols) < 2:
            return {'error': 'Necessário pelo menos 2 colunas numéricas'}
        
        corr_matrix = self.df[self.numeric_cols].corr()
        
        # Encontrar correlações mais fortes
        corr_pairs = []
        for i in range(len(corr_matrix)):
            for j in range(i+1, len(corr_matrix)):
                corr_pairs.append({
                    'var1': corr_matrix.index[i],
                    'var2': corr_matrix.columns[j],
                    'correlation': float(corr_matrix.iloc[i, j])
                })
        
        corr_pairs.sort(key=lambda x: abs(x['correlation']), reverse=True)
        
        return {
            'correlation_matrix': corr_matrix.to_dict(),
            'strongest_correlations': corr_pairs[:10],
            'interpretation': self._interpret_correlations(corr_pairs[:5])
        }
    
    def _interpret_correlations(self, top_corrs: List[Dict]) -> str:
        """Interpreta as correlações mais fortes"""
        interpretations = []
        for corr in top_corrs:
            strength = abs(corr['correlation'])
            direction = 'positiva' if corr['correlation'] > 0 else 'negativa'
            
            if strength > 0.8:
                level = 'muito forte'
            elif strength > 0.6:
                level = 'forte'
            elif strength > 0.4:
                level = 'moderada'
            else:
                level = 'fraca'
            
            interpretations.append(
                f"{corr['var1']} e {corr['var2']}: correlação {direction} {level} ({corr['correlation']:.3f})"
            )
        
        return '\n'.join(interpretations)
    
    def temporal_analysis(self, time_col: str, value_col: str) -> Dict[str, Any]:
        """Análise de tendências temporais"""
        if time_col not in self.df.columns or value_col not in self.df.columns:
            return {'error': 'Colunas especificadas não encontradas'}
        
        try:
            # Usar a coluna temporal como está (pode ser numérica ou datetime)
            df_temp = pd.DataFrame({
                'time': self.df[time_col],
                'value': self.df[value_col]
            }).dropna().sort_values('time')
            
            # Tendência linear simples
            x = np.arange(len(df_temp))
            y = df_temp['value'].values
            slope, intercept, r_value, _, _ = stats.linregress(x, y)
            
            return {
                'has_temporal_pattern': True,
                'trend': 'crescente' if slope > 0 else 'decrescente',
                'trend_strength': f"R² = {r_value**2:.3f}",
                'slope': float(slope),
                'data_points': int(len(df_temp)),
                'time_range': f"{df_temp['time'].min()} a {df_temp['time'].max()}"
            }
        except Exception as e:
            return {'error': f'Erro na análise temporal: {str(e)}'}
    
    def cluster_analysis(self, n_clusters: int = 3) -> Dict[str, Any]:
        """Análise de agrupamentos (clustering)"""
        if len(self.numeric_cols) < 2:
            return {'error': 'Necessário pelo menos 2 colunas numéricas'}
        
        # Preparar dados
        X = self.df[self.numeric_cols].dropna()
        if len(X) < n_clusters:
            return {'error': 'Dados insuficientes para clustering'}
        
        # Normalizar
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # KMeans
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)
        
        # Estatísticas por cluster
        cluster_stats = {}
        for i in range(n_clusters):
            cluster_data = X[labels == i]
            cluster_stats[f'cluster_{i}'] = {
                'size': int(len(cluster_data)),
                'percentage': f"{len(cluster_data)/len(X)*100:.1f}%",
                'means': {k: float(v) for k, v in cluster_data.mean().to_dict().items()}
            }
        
        return {
            'n_clusters': n_clusters,
            'cluster_stats': cluster_stats,
            'inertia': float(kmeans.inertia_),
            'warning': 'Clustering é exploratório - validar interpretação com conhecimento de domínio'
        }
