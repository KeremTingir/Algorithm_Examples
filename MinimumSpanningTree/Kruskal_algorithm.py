import heapq
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

# Union-Find veri yapısı (döngü kontrolü için)
def find(parent, i):
    if parent[i] != i:
        parent[i] = find(parent, parent[i])  # Path compression
    return parent[i]

def union(parent, rank, x, y):
    xroot = find(parent, x)
    yroot = find(parent, y)
    if rank[xroot] < rank[yroot]:
        parent[xroot] = yroot
    elif rank[xroot] > rank[yroot]:
        parent[yroot] = xroot
    else:
        parent[yroot] = xroot
        rank[xroot] += 1

# Kruskal Algoritması
def kruskal_mst(graph):
    mst = []
    edges = []
    
    # Tüm kenarları toplama
    for u in graph:
        for v, weight in graph[u].items():
            if u < v:  # Tekrar eklemeyi önlemek için
                edges.append((weight, u, v))
    
    # Kenarları ağırlığa göre sırala
    heapq.heapify(edges)
    
    # Union-Find için başlangıç
    nodes = list(graph.keys())
    parent = {node: node for node in nodes}
    rank = {node: 0 for node in nodes}
    
    while edges and len(mst) < len(nodes) - 1:
        weight, u, v = heapq.heappop(edges)
        if find(parent, u) != find(parent, v):
            union(parent, rank, u, v)
            mst.append((u, v, weight))
    
    return mst

# Grafı görselleştirme fonksiyonu
def visualize_graph(graph, mst, step, explanation, added_edge=None):
    G = nx.Graph()
    
    # Tüm kenarları ekle
    for u in graph:
        for v, weight in graph[u].items():
            G.add_edge(u, v, weight=weight)
    
    plt.figure(figsize=(10, 8))
    
    # Pozisyonları ayarla
    pos = nx.spring_layout(G)
    
    # MST kenarlarını yeşil, diğerlerini gri yap
    mst_edges = [(u, v) for u, v, _ in mst]
    all_edges = list(G.edges())
    non_mst_edges = [e for e in all_edges if e not in mst_edges and (e[1], e[0]) not in mst_edges]
    
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000)
    nx.draw_networkx_edges(G, pos, edgelist=mst_edges, edge_color='green', width=2)
    nx.draw_networkx_edges(G, pos, edgelist=non_mst_edges, edge_color='gray', width=1)
    
    # Yeni eklenen kenarı kırmızı ve kalın çiz
    if added_edge and added_edge[:2] in mst_edges:
        nx.draw_networkx_edges(G, pos, edgelist=[added_edge[:2]], edge_color='red', width=3)
    
    # Ağırlıkları etiketle
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_weight='bold')
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    
    plt.title(f"Kruskal Algoritması - Adım {step}\n{explanation}", fontsize=14, pad=20)
    plt.axis('off')
    plt.show()

# Test grafı
graph = {
    'A': {'B': 4, 'C': 2, 'D': 5},
    'B': {'A': 4, 'C': 1, 'E': 3},
    'C': {'A': 2, 'B': 1, 'D': 3, 'E': 4},
    'D': {'A': 5, 'C': 3, 'E': 2},
    'E': {'B': 3, 'C': 4, 'D': 2}
}

# Kruskal Algoritmasını uygula ve görselleştir
mst = []
edges = []

print("Adım 0: Başlangıç (Kenarlar sıralanıyor)")
visualize_graph(graph, mst, 0, "Kenarlar ağırlıklarına göre sıralanıyor.")

step = 1
mst = kruskal_mst(graph)
for i, (u, v, weight) in enumerate(mst, 1):
    print(f"\nAdım {i}: {u}-{v} kenarı (ağırlık: {weight}) eklendi")
    visualize_graph(graph, mst[:i], i, f"En düşük ağırlıklı kenar eklendi: {u}-{v} (ağırlık: {weight})", (u, v, weight))

print("\nMinimum Spanning Tree (MST):")
for u, v, weight in mst:
    print(f"{u}-{v}: {weight}")
print(f"Toplam ağırlık: {sum(weight for _, _, weight in mst)}")