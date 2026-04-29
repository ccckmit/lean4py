"""Machine Learning basics module."""

from typing import List, Tuple
import math


def linear_regression_ml(x: List[List[float]], y: List[float]) -> Tuple[List[float], float]:
    """Linear regression using least squares.
    
    Args:
        x: Input features (list of feature vectors)
        y: Target values
        
    Returns:
        (coefficients, intercept)
    """
    if not x or not y:
        return [], 0.0
    
    n = len(x)
    m = len(x[0]) if x else 0
    
    # Add bias term
    X = [[1.0] + row for row in x]
    beta = [0.0] * (m + 1)
    learning_rate = 0.01
    max_iter = 1000
    
    for _ in range(max_iter):
        # Compute gradient
        grad = [0.0] * (m + 1)
        for i in range(n):
            pred = sum(beta[j] * X[i][j] for j in range(m + 1))
            error = pred - y[i]
            for j in range(m + 1):
                grad[j] += error * X[i][j]
        
        # Update
        beta = [beta[j] - learning_rate * grad[j] / n for j in range(m + 1)]
    
    intercept = beta[0]
    coefficients = beta[1:]
    return coefficients, intercept


def logistic_regression(
    x: List[List[float]],
    y: List[int],
    learning_rate: float = 0.01,
    max_iter: int = 1000
) -> List[float]:
    """Logistic regression for binary classification.
    
    Args:
        x: Input features
        y: Binary labels (0 or 1)
        
    Returns:
        coefficients (including intercept)
    """
    n = len(x)
    m = len(x[0]) if x else 0
    
    # Add bias term
    X = [[1.0] + row for row in x]
    beta = [0.0] * (m + 1)
    
    for _ in range(max_iter):
        # Compute gradient of log-likelihood
        grad = [0.0] * (m + 1)
        for i in range(n):
            z = sum(beta[j] * X[i][j] for j in range(m + 1))
            p = 1 / (1 + math.exp(-z))
            error = y[i] - p
            for j in range(m + 1):
                grad[j] += error * X[i][j]
        
    # Update
    beta = [beta[j] + learning_rate * grad[j] / n for j in range(m + 1)]
    
    return beta


def svm_linear(
    x: List[List[float]],
    y: List[int],
    learning_rate: float = 0.01,
    max_iter: int = 1000,
    lambda_reg: float = 0.01
) -> List[float]:
    """Linear SVM using hinge loss with subgradient descent.
    
    Args:
        x: Input features
        y: Labels (-1 or 1)
        learning_rate: Learning rate for gradient descent
        max_iter: Maximum iterations
        lambda_reg: Regularization parameter
        
    Returns:
        weights (including bias as first element)
    """
    n = len(x)
    if n == 0:
        return []
    m = len(x[0])
    
    # Add bias term
    X = [[1.0] + row for row in x]
    w = [0.0] * (m + 1)
    
    for _ in range(max_iter):
        grad = [0.0] * (m + 1)
        for i in range(n):
            # Compute prediction
            pred = sum(w[j] * X[i][j] for j in range(m + 1))
            # Hinge loss subgradient
            if y[i] * pred < 1:
                for j in range(m + 1):
                    grad[j] -= y[i] * X[i][j]
            # Add regularization gradient
            if j > 0:  # Don't regularize bias
                grad[j] += lambda_reg * w[j]
        
        # Update weights
        w = [w[j] - learning_rate * grad[j] / n for j in range(m + 1)]
    
    return w


def _gini_impurity(labels: List[int]) -> float:
    """Compute Gini impurity for a set of labels."""
    if not labels:
        return 0.0
    n = len(labels)
    from collections import Counter
    counts = Counter(labels)
    impurity = 1.0
    for count in counts.values():
        prob = count / n
        impurity -= prob ** 2
    return impurity


def _split_data(
    x: List[List[float]],
    y: List[int],
    feature_idx: int,
    threshold: float
) -> Tuple[Tuple[List, List], Tuple[List, List]]:
    """Split data based on feature threshold."""
    left_x, left_y = [], []
    right_x, right_y = [], []
    for i in range(len(x)):
        if x[i][feature_idx] <= threshold:
            left_x.append(x[i])
            left_y.append(y[i])
        else:
            right_x.append(x[i])
            right_y.append(y[i])
    return (left_x, left_y), (right_x, right_y)


def decision_tree(
    x: List[List[float]],
    y: List[int],
    max_depth: int = 5
) -> dict:
    """Build a simple decision tree using CART algorithm.
    
    Args:
        x: Input features
        y: Labels (integers)
        max_depth: Maximum tree depth
        
    Returns:
        Tree represented as nested dict:
        {'leaf': True, 'label': label} or
        {'feature': idx, 'threshold': val, 'left': ..., 'right': ...}
    """
    def build_tree(x, y, depth):
        # Stopping conditions
        if len(set(y)) == 1 or depth >= max_depth or len(x) == 0:
            from collections import Counter
            label = Counter(y).most_common(1)[0][0] if y else 0
            return {'leaf': True, 'label': label}
        
        n_features = len(x[0]) if x else 0
        best_gini = float('inf')
        best_split = None
        
        # Find best split
        for feature_idx in range(n_features):
            values = set(row[feature_idx] for row in x)
            for threshold in values:
                (left_x, left_y), (right_x, right_y) = _split_data(
                    x, y, feature_idx, threshold
                )
                if not left_y or not right_y:
                    continue
                gini = (len(left_y) * _gini_impurity(left_y) + 
                       len(right_y) * _gini_impurity(right_y)) / len(y)
                if gini < best_gini:
                    best_gini = gini
                    best_split = (feature_idx, threshold, left_x, left_y, right_x, right_y)
        
        if best_split is None:
            from collections import Counter
            label = Counter(y).most_common(1)[0][0] if y else 0
            return {'leaf': True, 'label': label}
        
        feature_idx, threshold, left_x, left_y, right_x, right_y = best_split
        return {
            'leaf': False,
            'feature': feature_idx,
            'threshold': threshold,
            'left': build_tree(left_x, left_y, depth + 1),
            'right': build_tree(right_x, right_y, depth + 1)
        }
    
    return build_tree(x, y, 0)


def predict_tree(tree: dict, x: List[float]) -> int:
    """Predict using a decision tree."""
    if tree['leaf']:
        return tree['label']
    if x[tree['feature']] <= tree['threshold']:
        return predict_tree(tree['left'], x)
    else:
        return predict_tree(tree['right'], x)


def _euclidean_distance(a: List[float], b: List[float]) -> float:
    """Compute Euclidean distance between two vectors."""
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(len(a))))


def kmeans(
    data: List[List[float]],
    k: int,
    max_iter: int = 100,
    n_init: int = 10
) -> Tuple[List[List[float]], List[int]]:
    """K-means clustering algorithm.
    
    Args:
        data: List of data points (each point is a list of features)
        k: Number of clusters
        max_iter: Maximum iterations per initialization
        n_init: Number of times to run with different initializations
        
    Returns:
        (centroids, labels) where labels[i] is the cluster index for data[i]
    """
    import random
    
    if not data or k <= 0:
        return [], []
    
    n = len(data)
    dim = len(data[0])
    
    best_centroids = None
    best_labels = None
    best_inertia = float('inf')
    
    for _ in range(n_init):
        # Initialize centroids randomly from data points
        centroids = random.sample(data, k)
        
        labels = [0] * n
        
        for iteration in range(max_iter):
            # Assign points to nearest centroid
            new_labels = []
            for point in data:
                distances = [_euclidean_distance(point, c) for c in centroids]
                new_labels.append(distances.index(min(distances)))
            
            # Check convergence
            if new_labels == labels:
                labels = new_labels
                break
            labels = new_labels
            
            # Update centroids
            new_centroids = []
            for i in range(k):
                cluster_points = [data[j] for j in range(n) if labels[j] == i]
                if cluster_points:
                    centroid = [sum(p[d] for p in cluster_points) / len(cluster_points) 
                               for d in range(dim)]
                    new_centroids.append(centroid)
                else:
                    # Keep old centroid if cluster is empty
                    new_centroids.append(centroids[i])
            centroids = new_centroids
        
        # Compute inertia (sum of squared distances to assigned centroid)
        inertia = 0.0
        for j in range(n):
            centroid = centroids[labels[j]]
            inertia += _euclidean_distance(data[j], centroid) ** 2
        
        if inertia < best_inertia:
            best_inertia = inertia
            best_centroids = centroids
            best_labels = labels
    
    return best_centroids, best_labels


def random_forest(
    x: List[List[float]],
    y: List[int],
    n_trees: int = 10,
    max_depth: int = 5,
    sample_ratio: float = 0.7
) -> List[dict]:
    """Build a random forest classifier.
    
    Args:
        x: Input features
        y: Labels
        n_trees: Number of trees in the forest
        max_depth: Maximum depth per tree
        sample_ratio: Ratio of data to sample for each tree (with replacement)
        
    Returns:
        List of decision trees
    """
    import random
    
    n = len(x)
    if n == 0:
        return []
    
    trees = []
    for _ in range(n_trees):
        # Bootstrap sample
        sample_size = int(n * sample_ratio)
        indices = [random.randint(0, n-1) for _ in range(sample_size)]
        sample_x = [x[i] for i in indices]
        sample_y = [y[i] for i in indices]
        
        # Build tree
        tree = decision_tree(sample_x, sample_y, max_depth=max_depth)
        trees.append(tree)
    
    return trees


def predict_random_forest(trees: List[dict], x: List[float]) -> int:
    """Predict using a random forest (majority vote).
    
    Args:
        trees: List of decision trees from random_forest()
        x: Input features
        
    Returns:
        Predicted class label
    """
    if not trees:
        return 0
    
    # Get predictions from all trees
    predictions = [predict_tree(tree, x) for tree in trees]
    
    # Majority vote
    from collections import Counter
    return Counter(predictions).most_common(1)[0][0]
