import matplotlib.pyplot as plt
import networkx as nx
import heapq
import random
from collections import defaultdict

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

def create_random_graph(num_nodes):
    # Yönsüz, bağlantılı, ağırlıklı graf oluştur
    graph = {chr(65 + i): {} for i in range(num_nodes)}  # Düğümler: A, B, C, ...
    
    # Minimum bağlantılılık için bir spanning tree oluştur
    nodes = list(graph.keys())
    random.shuffle(nodes)
    for i in range(1, num_nodes):
        u = nodes[i]
        v = nodes[random.randint(0, i-1)]  # Önceki düğümlerden rastgele birini seç
        weight = random.randint(1, 10)
        graph[u][v] = weight
        graph[v][u] = weight
    
    # Ekstra kenarlar ekle (rastgele, grafın yoğunluğunu artırmak için)
    for _ in range(num_nodes * 2):  # Ortalama 2 ek kenar/düğüm
        u, v = random.sample(nodes, 2)
        if v not in graph[u] and random.random() < 0.5:  # %50 olasılıkla ekle
            weight = random.randint(1, 10)
            graph[u][v] = weight
            graph[v][u] = weight
    
    return graph

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
            yield u, v, weight  # Her adım için kenar bilgisi döndür

def visualize_graph(graph, mst, step, explanation, added_edge=None):
    G = nx.Graph()
    
    # Tüm kenarları ekle
    for u in graph:
        for v, weight in graph[u].items():
            if (u, v) not in G.edges() and (v, u) not in G.edges():
                G.add_edge(u, v, weight=weight)
    
    plt.figure(figsize=(10, 8))
    
    # Pozisyonları ayarla
    pos = nx.spring_layout(G, seed=42)
    
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

def main():
    try:
        num_nodes = int(input("Düğüm sayısını girin (örneğin, 10): "))
        if num_nodes <= 0:
            print("Düğüm sayısı pozitif olmalıdır!")
            return
    except ValueError:
        print("Geçerli bir sayı girin!")
        return

    # Rastgele graf oluştur
    graph = create_random_graph(num_nodes)
    print("\nOluşturulan Graf (Kenar: Ağırlık):")
    for u in graph:
        for v, weight in graph[u].items():
            if u < v:  # Her kenarı bir kez yazdır
                print(f"{u}-{v}: {weight}")

    # Başlangıç grafı
    mst = []
    print(f"\nAdım 0: Başlangıç (Kenarlar sıralanıyor)")
    visualize_graph(graph, mst, 0, "Kenarlar ağırlıklarına göre sıralanıyor.")

    # Kruskal algoritmasını adım adım uygula
    step = 1
    for u, v, weight in kruskal_mst(graph):
        mst.append((u, v, weight))
        print(f"\nAdım {step}: {u}-{v} kenarı (ağırlık: {weight}) eklendi")
        visualize_graph(graph, mst, step, f"En düşük ağırlıklı kenar eklendi: {u}-{v} (ağırlık: {weight})", (u, v, weight))
        step += 1

    print("\nMinimum Spanning Tree (MST):")
    for u, v, weight in mst:
        print(f"{u}-{v}: {weight}")
    print(f"Toplam ağırlık: {sum(weight for _, _, weight in mst)}")

if __name__ == "__main__":
    main()