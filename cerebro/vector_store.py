import chromadb
import time
from chromadb.utils import embedding_functions

from .ingester import CerebroChunk

class CerebroVectorStore:
    def __init__(self, db_path="./data/chroma_db"):
        self.emb_fn = embedding_functions.DefaultEmbeddingFunction()
        
        # Initialize persistent client
        self.client = chromadb.PersistentClient(path=db_path)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="cerebro_docs", 
            embedding_function=self.emb_fn
        )

    def add_chunks(self, chunks):
        """Adds chunks to the database with metadata."""
        if not chunks:
            return
        
        ids = [c.chunk_id for c in chunks]
        documents = [c.text for c in chunks]
        
        metadatas = []
        for c in chunks:
            # Safely get timestamp, default to now if missing
            ts = getattr(c, "timestamp", time.time())
            
            metadatas.append({
                "source": c.source,
                "page": str(c.page),     
                "timestamp": float(ts)   
            })
        
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

    def search(self, query, n_results=5, source_filter=None):
        """
        Searches for relevant chunks with optional filtering.
        source_filter: list of filenames (strings) to restrict search scope.
        """
        where_clause = None
        
        # Build ChromaDB filter query if a filter is provided
        if source_filter and len(source_filter) > 0:
            if len(source_filter) == 1:
                # Filter by single file
                where_clause = {"source": source_filter[0]}
            else:
                # Filter by list of files using $in operator
                where_clause = {"source": {"$in": source_filter}}

        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_clause # Apply the filter
        )
        return results