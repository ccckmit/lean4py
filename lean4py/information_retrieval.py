"""Information Retrieval module for document search and ranking."""

from typing import List, Tuple, Dict
import math


class TFIDF:
    """TF-IDF (Term Frequency-Inverse Document Frequency) vectorizer."""
    
    def __init__(self, max_features: int = 1000):
        self.max_features = max_features
        self.vocabulary: Dict[str, int] = {}
        self.idf: List[float] = []
    
    def fit(self, documents: List[str]):
        """Build vocabulary and compute IDF values.
        
        Args:
            documents: List of text documents
        """
        # Tokenize
        doc_tokens = [self._tokenize(doc) for doc in documents]
        
        # Count document frequencies
        doc_freq = {}
        for tokens in doc_tokens:
            for token in set(tokens):
                doc_freq[token] = doc_freq.get(token, 0) + 1
        
        # Select top features by document frequency
        sorted_tokens = sorted(doc_freq.items(), key=lambda x: x[1], reverse=True)
        self.vocabulary = {token: idx for idx, (token, _) 
                          in enumerate(sorted_tokens[:self.max_features])}
        
        # Compute IDF
        n_docs = len(documents)
        self.idf = []
        for token in self.vocabulary:
            df = doc_freq.get(token, 0)
            self.idf.append(math.log((n_docs + 1) / (df + 1)) + 1)
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization."""
        return text.lower().split()
    
    def transform(self, documents: List[str]) -> List[List[float]]:
        """Transform documents to TF-IDF vectors."""
        if not self.vocabulary:
            return []
        
        n_features = len(self.vocabulary)
        vectors = []
        
        for doc in documents:
            tokens = self._tokenize(doc)
            tf = {}
            for token in tokens:
                if token in self.vocabulary:
                    tf[token] = tf.get(token, 0) + 1
            
            # Compute TF-IDF
            vector = [0.0] * n_features
            for token, count in tf.items():
                idx = self.vocabulary[token]
                tf_value = count / max(len(tokens), 1)
                vector[idx] = tf_value * self.idf[idx]
            
            vectors.append(vector)
        
        return vectors
    
    def fit_transform(self, documents: List[str]) -> List[List[float]]:
        """Fit and transform in one step."""
        self.fit(documents)
        return self.transform(documents)


class BM25:
    """Okapi BM25 ranking function."""
    
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.vocabulary: Dict[str, int] = {}
        self.avgdl = 0.0
        self.doc_freqs: List[Dict[str, int]] = []
        self.doc_lengths: List[int] = []
    
    def fit(self, documents: List[str]):
        """Build index for BM25."""
        total_len = 0
        
        for doc in documents:
            tokens = doc.lower().split()
            self.doc_lengths.append(len(tokens))
            total_len += len(tokens)
            
            df = {}
            for token in set(tokens):
                df[token] = df.get(token, 0) + 1
            
            self.doc_freqs.append(df)
            
            for token in df:
                if token not in self.vocabulary:
                    self.vocabulary[token] = len(self.vocabulary)
        
        self.avgdl = total_len / max(len(documents), 1)
    
    def score(self, query: str, doc_idx: int) -> float:
        """Compute BM25 score for query-document pair."""
        tokens = query.lower().split()
        doc_df = self.doc_freqs[doc_idx]
        doc_len = self.doc_lengths[doc_idx]
        n_docs = len(self.doc_freqs)
        
        score = 0.0
        for token in tokens:
            if token not in self.vocabulary:
                continue
            
            df = doc_df.get(token, 0)
            if df == 0:
                continue
            
            idf = math.log((n_docs - df + 0.5) / (df + 0.5) + 1)
            
            tf = df  # Use document frequency as proxy for term frequency
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)
            
            score += idf * numerator / denominator
        
        return score
    
    def rank(self, query: str, top_k: int = 10) -> List[Tuple[int, float]]:
        """Rank documents by BM25 score."""
        scores = [(i, self.score(query, i)) for i in range(len(self.doc_freqs))]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Compute cosine similarity between two vectors.
    
    Args:
        a, b: Feature vectors
        
    Returns:
        Cosine similarity in [-1, 1]
    """
    if not a or not b or len(a) != len(b):
        return 0.0
    
    dot_prod = sum(a[i] * b[i] for i in range(len(a)))
    norm_a = math.sqrt(sum(a[i]**2 for i in range(len(a))))
    norm_b = math.sqrt(sum(b[i]**2 for i in range(len(b))))
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return dot_prod / (norm_a * norm_b)


def retrieve(
    query_vector: List[float],
    document_vectors: List[List[float]],
    top_k: int = 10
) -> List[Tuple[int, float]]:
    """Retrieve most similar documents using cosine similarity.
    
    Args:
        query_vector: Query vector
        document_vectors: List of document vectors
        top_k: Number of results to return
        
    Returns:
        List of (doc_index, similarity_score) tuples
    """
    scores = [(i, cosine_similarity(query_vector, doc)) 
              for i, doc in enumerate(document_vectors)]
    
    scores.sort(key=lambda x: x[1], reverse=True)
    
    return scores[:top_k]


def build_inverted_index(
    documents: List[str]
) -> Dict[str, List[int]]:
    """Build simple inverted index for fast retrieval.
    
    Args:
        documents: List of documents
        
    Returns:
        Dictionary mapping terms to document IDs
    """
    index: Dict[str, List[int]] = {}
    
    for doc_id, doc in enumerate(documents):
        tokens = set(doc.lower().split())
        for token in tokens:
            if token not in index:
                index[token] = []
            index[token].append(doc_id)
    
    return index