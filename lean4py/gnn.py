"""Graph Neural Network module for graph representation learning."""

from typing import List, Tuple, Optional, Callable
import math


class MessagePassing:
    """Base class for message passing neural networks."""
    
    def __init__(self, node_features: int, hidden_dim: int):
        self.node_features = node_features
        self.hidden_dim = hidden_dim
    
    def aggregate(self, messages: List[float], neighbors: List[int]) -> float:
        """Aggregate messages from neighbors."""
        if not messages:
            return 0.0
        return sum(messages) / len(messages)
    
    def update(self, node_embedding: float, aggregated: float) -> float:
        """Update node embedding."""
        return node_embedding + aggregated


class GCNLayer(MessagePassing):
    """Graph Convolutional Network layer.
    
    H' = Activation(D^{-1/2} A D^{-1/2} H W)
    """
    
    def __init__(self, node_features: int, output_dim: int):
        super().__init__(node_features, output_dim)
        self.output_dim = output_dim
        
        # Simple weight matrix
        import random
        self.W = [[random.gauss(0, 0.1) for _ in range(output_dim)]
                  for _ in range(node_features)]
    
    def forward(
        self,
        node_features: List[List[float]],
        edges: List[Tuple[int, int]]
    ) -> List[List[float]]:
        """Forward pass through GCN layer.
        
        Args:
            node_features: Node feature matrix (n_nodes x node_features)
            edges: List of edges (undirected)
            
        Returns:
            Updated node features (n_nodes x output_dim)
        """
        n_nodes = len(node_features)
        
        # Build adjacency matrix
        adj = [[0.0] * n_nodes for _ in range(n_nodes)]
        for i, j in edges:
            adj[i][j] = 1.0
            adj[j][i] = 1.0
        
        # Add self-loops
        for i in range(n_nodes):
            adj[i][i] = 1.0
        
        # Compute degree matrix
        degree = [sum(adj[i]) for i in range(n_nodes)]
        
        # Compute D^{-1/2} A D^{-1/2}
        normalized = [[0.0] * n_nodes for _ in range(n_nodes)]
        for i in range(n_nodes):
            for j in range(n_nodes):
                if degree[i] > 0 and degree[j] > 0:
                    normalized[i][j] = adj[i][j] / (math.sqrt(degree[i]) * math.sqrt(degree[j]))
        
        # Compute H' = normalized @ H @ W
        H = node_features
        HW = [[sum(H[i][k] * self.W[k][j] for k in range(len(self.W)))
               for j in range(self.output_dim)]
              for i in range(n_nodes)]
        
        output = [[sum(normalized[i][j] * HW[j][d] for j in range(n_nodes))
                   for d in range(self.output_dim)]
                  for i in range(n_nodes)]
        
        # Activation (ReLU)
        output = [[max(0.0, val) for val in row] for row in output]
        
        return output


class GraphAttentionLayer(MessagePassing):
    """Graph Attention Network layer.
    
    Uses attention coefficients to weight neighbor contributions.
    """
    
    def __init__(self, node_features: int, output_dim: int, n_heads: int = 4):
        super().__init__(node_features, output_dim)
        self.output_dim = output_dim
        self.n_heads = n_heads
        
        import random
        self.W = [[random.gauss(0, 0.1) for _ in range(output_dim)]
                  for _ in range(node_features)]
        self.a = [random.gauss(0, 0.1) for _ in range(output_dim * 2)]
    
    def attention_score(self, h_i: List[float], h_j: List[float]) -> float:
        """Compute attention coefficient between two nodes."""
        concat = h_i + h_j
        score = sum(self.a[k] * concat[k] for k in range(len(concat)))
        return math.exp(max(score, 0))  # LeakyReLU + softmax
    
    def forward(
        self,
        node_features: List[List[float]],
        edges: List[Tuple[int, int]]
    ) -> List[List[float]]:
        """Forward pass through GAT layer."""
        n_nodes = len(node_features)
        
        # Build adjacency with attention
        adj_attention = [[0.0] * n_nodes for _ in range(n_nodes)]
        
        for i in range(n_nodes):
            neighbors = [j for j in range(n_nodes) if (i, j) in edges or (j, i) in edges]
            if not neighbors:
                neighbors = [i]  # Self-loop if no neighbors
            
            # Compute attention for each neighbor
            for j in neighbors:
                score = self.attention_score(node_features[i], node_features[j])
                adj_attention[i][j] = score
        
        # Normalize attention
        for i in range(n_nodes):
            row_sum = sum(adj_attention[i])
            if row_sum > 0:
                for j in range(n_nodes):
                    adj_attention[i][j] /= row_sum
        
        # Compute output
        HW = [[sum(node_features[i][k] * self.W[k][j]
                   for k in range(len(self.W)))
               for j in range(self.output_dim)]
              for i in range(n_nodes)]
        
        output = [[sum(adj_attention[i][j] * HW[j][d] for j in range(n_nodes))
                   for d in range(self.output_dim)]
                  for i in range(n_nodes)]
        
        # Activation
        output = [[max(0.0, val) for val in row] for row in output]
        
        return output


def graph_pooling(
    node_embeddings: List[List[float]],
    method: str = 'mean'
) -> List[float]:
    """Pool node embeddings to graph embedding.
    
    Args:
        node_embeddings: List of node feature vectors
        method: Pooling method ('mean', 'max', 'sum')
        
    Returns:
        Graph-level embedding
    """
    if not node_embeddings:
        return []
    
    n_features = len(node_embeddings[0])
    
    if method == 'mean':
        return [sum(node_embeddings[i][d] for i in range(len(node_embeddings))) / len(node_embeddings)
                for d in range(n_features)]
    elif method == 'max':
        return [max(node_embeddings[i][d] for i in range(len(node_embeddings)))
                for d in range(n_features)]
    elif method == 'sum':
        return [sum(node_embeddings[i][d] for i in range(len(node_embeddings)))
                for d in range(n_features)]
    else:
        return graph_pooling(node_embeddings, 'mean')


def node_classification(
    node_features: List[List[float]],
    edges: List[Tuple[int, int]],
    labels: List[int],
    n_classes: int = 2,
    hidden_dim: int = 16,
    n_epochs: int = 100
) -> List[int]:
    """Simple node classification using GCN.
    
    Args:
        node_features: Node feature matrix
        edges: Graph edges
        labels: Known labels (0 for unknown)
        n_classes: Number of classes
        hidden_dim: Hidden layer dimension
        n_epochs: Training epochs
        
    Returns:
        Predicted labels for all nodes
    """
    n_nodes = len(node_features)
    node_dim = len(node_features[0])
    
    # Create GCN layers
    gcn1 = GCNLayer(node_dim, hidden_dim)
    gcn2 = GCNLayer(hidden_dim, n_classes)
    
    for _ in range(n_epochs):
        # Forward through GCN layers
        hidden = gcn1.forward(node_features, edges)
        logits = gcn2.forward(hidden, edges)
        
        # Simple gradient descent for known labels
        for i in range(n_nodes):
            if labels[i] >= 0:  # Known label
                for c in range(n_classes):
                    target = 1.0 if c == labels[i] else 0.0
                    for d in range(n_classes):
                        # Simple update
                        gcn2.W[c][d] -= 0.01 * (logits[i][d] - target) * hidden[i][c]
    
    # Final predictions
    hidden = gcn1.forward(node_features, edges)
    logits = gcn2.forward(hidden, edges)
    
    predictions = [logits[i].index(max(logits[i])) for i in range(n_nodes)]
    
    return predictions