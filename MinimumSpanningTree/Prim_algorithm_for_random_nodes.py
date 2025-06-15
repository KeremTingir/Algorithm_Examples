import matplotlib.pyplot as plt
import networkx as nx
import heapq
import random

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
    
    plt.title(f"Prim Algoritması - Adım {step}\n{explanation}", fontsize=14, pad=20)
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

    # Başlangıç düğümü
    start_node = chr(65)  # 'A'
    mst = []
    visited = set()

    print(f"\nAdım 0: Başlangıç (Düğüm {start_node} ile başlanıyor)")
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

if __name__ == "__main__":
    main()