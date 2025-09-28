from __future__ import annotations

import math


def mean_predict(train_y: list[float], test_x: list[list[float]]) -> list[float]:
    value = sum(train_y) / len(train_y)
    return [value] * len(test_x)


def _standardize(train_x: list[list[float]], test_x: list[list[float]]):
    width = len(train_x[0])
    means = [sum(row[j] for row in train_x) / len(train_x) for j in range(width)]
    scales = []
    for j in range(width):
        variance = sum((row[j] - means[j]) ** 2 for row in train_x) / len(train_x)
        scales.append(math.sqrt(variance) or 1.0)
    transform = lambda rows: [[(row[j] - means[j]) / scales[j] for j in range(width)] for row in rows]
    return transform(train_x), transform(test_x)


def knn_predict(train_x: list[list[float]], train_y: list[float], test_x: list[list[float]], k: int = 3):
    train_z, test_z = _standardize(train_x, test_x)
    predictions = []
    for query in test_z:
        distances = []
        for features, target in zip(train_z, train_y):
            distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(query, features)))
            distances.append((distance, target))
        neighbors = sorted(distances)[: min(k, len(distances))]
        weights = [1.0 / (distance + 1e-9) for distance, _ in neighbors]
        predictions.append(sum(w * item[1] for w, item in zip(weights, neighbors)) / sum(weights))
    return predictions


def _solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    n = len(vector)
    augmented = [matrix[i][:] + [vector[i]] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(augmented[row][col]))
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        divisor = augmented[col][col]
        if abs(divisor) < 1e-12:
            continue
        augmented[col] = [value / divisor for value in augmented[col]]
        for row in range(n):
            if row == col:
                continue
            factor = augmented[row][col]
            augmented[row] = [a - factor * b for a, b in zip(augmented[row], augmented[col])]
    return [augmented[i][-1] for i in range(n)]


def ridge_predict(
    train_x: list[list[float]], train_y: list[float], test_x: list[list[float]], alpha: float = 1.0
) -> list[float]:
    train_z, test_z = _standardize(train_x, test_x)
    target_mean = sum(train_y) / len(train_y)
    centered = [value - target_mean for value in train_y]
    width = len(train_z[0])
    gram = [[sum(row[i] * row[j] for row in train_z) for j in range(width)] for i in range(width)]
    for i in range(width):
        gram[i][i] += alpha
    rhs = [sum(row[i] * target for row, target in zip(train_z, centered)) for i in range(width)]
    weights = _solve(gram, rhs)
    return [target_mean + sum(w * x for w, x in zip(weights, row)) for row in test_z]
