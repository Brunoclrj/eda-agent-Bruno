"""
Memory Store - Sistema de memória persistente para análises e conclusões
"""
import chromadb
from chromadb.config import Settings
import sqlite3
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
import os


class MemoryStore:
    """Sistema de memória persistente"""
    
    def __init__(self, persist_dir: str = "./data/memory"):
        os.makedirs(persist_dir, exist_ok=True)
        
        # ChromaDB para busca semântica
        self.chroma_client = chromadb.Client(Settings(
            persist_directory=persist_dir,
            anonymized_telemetry=False
        ))
        
        self.collection = self.chroma_client.get_or_create_collection(
            name="eda_analyses",
            metadata={"description": "Análises e conclusões de datasets"}
        )
        
        # SQLite para metadata estruturado
        self.db_path = f"{persist_dir}/metadata.db"
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init_db()
    
    def _init_db(self):
        """Inicializa schema do banco"""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id TEXT PRIMARY KEY,
                dataset_hash TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                question TEXT,
                analysis_type TEXT,
                results TEXT,
                conclusions TEXT,
                has_plot BOOLEAN
            )
        """)
        
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS datasets (
                hash TEXT PRIMARY KEY,
                filename TEXT,
                columns TEXT,
                shape TEXT,
                uploaded_at TEXT
            )
        """)
        self.conn.commit()
    
    def register_dataset(self, filepath: str, metadata: Dict) -> str:
        """Registra novo dataset"""
        dataset_hash = self._hash_dataset(filepath, metadata)
        
        self.conn.execute("""
            INSERT OR REPLACE INTO datasets (hash, filename, columns, shape, uploaded_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            dataset_hash,
            filepath,
            json.dumps(metadata['columns']),
            json.dumps(metadata['shape']),
            datetime.now().isoformat()
        ))
        self.conn.commit()
        
        return dataset_hash
    
    def _hash_dataset(self, filepath: str, metadata: Dict) -> str:
        """Gera hash único do dataset"""
        content = f"{filepath}_{json.dumps(sorted(metadata['columns']))}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def store_analysis(
        self,
        dataset_hash: str,
        question: str,
        analysis_type: str,
        results: Dict[str, Any],
        conclusions: str,
        has_plot: bool = False
    ) -> str:
        """Armazena análise completa"""
        
        analysis_id = hashlib.md5(
            f"{dataset_hash}_{question}_{datetime.now().isoformat()}".encode()
        ).hexdigest()
        
        # Armazenar em SQLite
        self.conn.execute("""
            INSERT INTO analyses 
            (id, dataset_hash, timestamp, question, analysis_type, results, conclusions, has_plot)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            analysis_id,
            dataset_hash,
            datetime.now().isoformat(),
            question,
            analysis_type,
            json.dumps(results),
            conclusions,
            has_plot
        ))
        self.conn.commit()
        
        # Armazenar em Chroma para busca semântica
        try:
            self.collection.add(
                documents=[conclusions],
                metadatas=[{
                    "dataset_hash": dataset_hash,
                    "question": question,
                    "analysis_type": analysis_type,
                    "timestamp": datetime.now().isoformat()
                }],
                ids=[analysis_id]
            )
        except Exception as e:
            print(f"Aviso: Erro ao adicionar ao Chroma: {e}")
        
        return analysis_id
    
    def get_conclusions(self, dataset_hash: str, limit: int = 10) -> List[Dict]:
        """Recupera conclusões para um dataset"""
        cursor = self.conn.execute("""
            SELECT question, analysis_type, conclusions, timestamp, has_plot
            FROM analyses
            WHERE dataset_hash = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (dataset_hash, limit))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'question': row[0],
                'analysis_type': row[1],
                'conclusions': row[2],
                'timestamp': row[3],
                'has_plot': bool(row[4])
            })
        
        return results
    
    def search_similar_analyses(
        self, 
        query: str, 
        dataset_hash: Optional[str] = None, 
        n_results: int = 5
    ) -> List[Dict]:
        """Busca análises similares (RAG)"""
        try:
            where_filter = {"dataset_hash": dataset_hash} if dataset_hash else None
            
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where_filter
            )
            
            if not results['documents'][0]:
                return []
            
            return [{
                'document': doc,
                'metadata': meta,
                'distance': dist
            } for doc, meta, dist in zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            )]
        except Exception as e:
            print(f"Aviso: Erro na busca semântica: {e}")
            return []
