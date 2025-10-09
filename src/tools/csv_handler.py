"""
CSV Handler - Carregamento robusto de qualquer CSV
"""
import pandas as pd
import chardet
import duckdb
from typing import Dict, Any, Optional
import re
import hashlib


class CSVHandler:
    """Handler robusto para qualquer CSV"""
    
    def __init__(self):
        self.df: Optional[pd.DataFrame] = None
        self.metadata: Dict[str, Any] = {}
        self.conn = duckdb.connect(':memory:')
        self.filepath: str = ""
    
    def load_csv(self, filepath: str, sample_size: int = 10000) -> pd.DataFrame:
        """Carrega CSV com detecção automática de encoding e delimiter"""
        
        self.filepath = filepath
        
        # 1. Detectar encoding
        with open(filepath, 'rb') as f:
            raw = f.read(100000)  # Primeiros 100KB
        detected = chardet.detect(raw)
        encoding = detected['encoding'] or 'utf-8'
        
        # 2. Detectar delimiter
        with open(filepath, 'r', encoding=encoding, errors='ignore') as f:
            first_line = f.readline()
        delimiter = self._detect_delimiter(first_line)
        
        # 3. Carregar com pandas
        try:
            self.df = pd.read_csv(
                filepath,
                encoding=encoding,
                sep=delimiter,
                low_memory=False,
                nrows=sample_size if sample_size > 0 else None
            )
        except Exception as e:
            # Fallback: tentar com engine python
            self.df = pd.read_csv(
                filepath,
                encoding=encoding,
                sep=delimiter,
                engine='python',
                on_bad_lines='skip',
                nrows=sample_size if sample_size > 0 else None
            )
        
        # 4. Normalizar headers
        self.df.columns = [self._normalize_column_name(col) for col in self.df.columns]
        
        # 5. Gerar metadata
        self.metadata = self._generate_metadata()
        
        # 6. Registrar no DuckDB para queries SQL
        self.conn.register('data', self.df)
        
        return self.df
    
    def _detect_delimiter(self, line: str) -> str:
        """Detecta o delimitador mais provável"""
        delimiters = [',', ';', '\t', '|']
        counts = {d: line.count(d) for d in delimiters}
        return max(counts, key=counts.get)
    
    def _normalize_column_name(self, col: str) -> str:
        """Normaliza nome de coluna"""
        col = str(col).strip()
        col = re.sub(r'[^\w\s-]', '', col)
        col = re.sub(r'[-\s]+', '_', col)
        return col.lower()
    
    def _generate_metadata(self) -> Dict[str, Any]:
        """Gera metadata completo do dataset"""
        meta = {
            'shape': self.df.shape,
            'columns': list(self.df.columns),
            'dtypes': self.df.dtypes.astype(str).to_dict(),
            'missing': self.df.isnull().sum().to_dict(),
            'memory_mb': self.df.memory_usage(deep=True).sum() / 1024**2,
        }
        
        # Classificar colunas por tipo
        numeric_cols = self.df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        datetime_cols = self.df.select_dtypes(include=['datetime']).columns.tolist()
        
        meta['column_types'] = {
            'numeric': numeric_cols,
            'categorical': categorical_cols,
            'datetime': datetime_cols
        }
        
        # Estatísticas básicas para colunas numéricas
        if numeric_cols:
            meta['numeric_stats'] = self.df[numeric_cols].describe().to_dict()
        
        # Cardinalidade para categóricas
        if categorical_cols:
            meta['categorical_cardinality'] = {
                col: self.df[col].nunique() for col in categorical_cols[:10]  # Limitar a 10
            }
        
        return meta
    
    def query(self, sql: str) -> pd.DataFrame:
        """Executa query SQL no dataset"""
        return self.conn.execute(sql).df()
    
    def get_sample(self, n: int = 100) -> pd.DataFrame:
        """Retorna amostra aleatória"""
        return self.df.sample(min(n, len(self.df)))
    
    def get_hash(self) -> str:
        """Retorna hash único do dataset"""
        content = f"{self.filepath}_{json.dumps(sorted(self.metadata['columns']))}"
        return hashlib.md5(content.encode()).hexdigest()
