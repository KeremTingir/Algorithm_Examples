import heapq
import networkx as nx
import matplotlib.pyplot as plt

# Prim Algoritması
def prim_mst(graph, start_node):
    mst = []
    visited = {start_node}
    edges = [(weight, start_node, to) for to, weight in graph[start_node].items()]
    heapq.heapify(edges)
    
    while edges:
        weight, u, v = heapq.heappop(edges)
        if v not in visited:
            visited.add(v)
            mst.append((u, v, weight))
            
            for next_node, next_weight in graph[v].items():
                if next_node not in visited:
                    heapq.heappush(edges, (next_weight, v, next_node))
    
    return mst

# Ağacı görselleştirme fonksiyonu
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
    
    plt.title(f"Prim Algoritması - Adım {step}\n{explanation}", fontsize=14, pad=20)
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

# Prim Algoritmasını uygula ve görselleştir
start_node = 'A'
mst = []
visited = set()

print(f"Adım 0: Başlangıç (Düğüm {start_node} ile başlanıyor)")
visualize_graph(graph, mst, 0, f"Başlangıç noktası: {start_node}")

step = 1
visited.add(start_node)
edges = [(weight, start_node, to) for to, weight in graph[start_node].items()]
heapq.heapify(edges)

while edges:
    weight, u, v = heapq.heappop(edges)
    if v not in visited:
        visited.add(v)
        mst.append((u, v, weight))
        print(f"\nAdım {step}: {u}-{v} kenarı (ağırlık: {weight}) eklendi")
        visualize_graph(graph, mst, step, f"En düşük ağırlıklı kenar eklendi: {u}-{v} (ağırlık: {weight})", (u, v, weight))
        step += 1
        
        for next_node, next_weight in graph[v].items():
            if next_node not in visited:
                heapq.heappush(edges, (next_weight, v, next_node))

print("\nMinimum Spanning Tree (MST):")
for u, v, weight in mst:
    print(f"{u}-{v}: {weight}")
print(f"Toplam ağırlık: {sum(weight for _, _, weight in mst)}")