import pandas as pd
import networkx as nx
import numpy as np

# Load the data
data = pd.read_csv('D:\Anurag\Development\srfp projects\project2\impressive_people.csv')

# Create the graph
G = nx.DiGraph()
for i, row in data.iterrows():
    person = row[0]
    impressives = row[1:].dropna().tolist()
    for impressive in impressives:
        G.add_edge(person, impressive)

# Function to handle sinkholes
def handle_sinkholes(scores, N):
    sink_value = scores.sum() / N
    scores = scores.apply(lambda x: x + sink_value)
    return scores

# Random Walk (PageRank) Algorithm with normalization
def random_walk_pagerank(G, alpha=0.85, max_iter=100, tol=1.0e-6):
    nodes = G.nodes()
    N = len(nodes)
    rank = pd.Series(np.ones(N) / N, index=nodes)
    sink_value = (1.0 - alpha) / N
    
    for _ in range(max_iter):
        rank_new = rank.copy() * (1 - alpha) / N
        for node in nodes:
            neighbors = list(G.neighbors(node))
            if neighbors:
                for neighbor in neighbors:
                    rank_new[neighbor] += alpha * rank[node] / len(neighbors)
        
        # Handle sinkholes
        rank_new = handle_sinkholes(rank_new, N)
        
        # Normalize the ranks
        rank_new = rank_new / rank_new.sum()
        
        # Check for convergence
        if np.abs(rank_new - rank).sum() < tol:
            break
        rank = rank_new
    
    return rank.sort_values(ascending=False)

# Equal Points Distribution Algorithm with normalization
def equal_points_distribution(G, max_iter=100, tol=1.0e-6):
    nodes = G.nodes()
    N = len(nodes)
    points = pd.Series(np.ones(N), index=nodes)
    
    for _ in range(max_iter):
        points_new = pd.Series(np.zeros(N), index=nodes)
        for node in nodes:
            neighbors = list(G.neighbors(node))
            if neighbors:
                share = points[node] / len(neighbors)
                for neighbor in neighbors:
                    points_new[neighbor] += share
        
        # Handle sinkholes
        points_new = handle_sinkholes(points_new, N)
        
        # Normalize the points
        points_new = points_new / points_new.sum()
        
        # Check for convergence
        if np.abs(points_new - points).sum() < tol:
            break
        points = points_new
    
    return points.sort_values(ascending=False)

# Compute ranks using both algorithms
pagerank_result = random_walk_pagerank(G)
epd_result = equal_points_distribution(G)

# Extract top 10 nodes
top_10_pagerank = pagerank_result.head(10)
top_10_epd = epd_result.head(10)

print("Top 10 most important persons using Random Walk (PageRank) Algorithm:")
print(top_10_pagerank)

print("\nTop 10 most important persons using Equal Points Distribution Algorithm:")
print(top_10_epd)
