import matplotlib.pyplot as plt
import networkx as nx

def get_fixed_graph():
    # Sabit graf: (u, v, ağırlık)
    graph = [
        (0, 1, 4),
        (0, 2, -2),
        (1, 3, 2),
        (2, 1, 1),
        (2, 3, 5)
    ]
    return graph

def draw_graph(graph, num_nodes):
    G = nx.DiGraph()
    for i in range(num_nodes):
        G.add_node(i)
    for u, v, w in graph:
        G.add_edge(u, v, weight=w)

    pos = nx.spring_layout(G, seed=42)  # Sabit yerleşim
    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
    nx.draw_networkx_labels(G, pos, font_size=10)
    nx.draw_networkx_edges(G, pos, edge_color='black', arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): w for u, v, w in graph}, font_size=8)
    
    plt.title("Tanımlı Graf")
    plt.show()

def draw_table(distances, predecessors, step, edge=None):
    num_nodes = 4  # Sabit düğüm sayısı
    # Tablo verileri
    data = [[i, str(distances[i]) if distances[i] != float('inf') else '∞', 
             str(predecessors[i]) if predecessors[i] is not None else '-']
            for i in range(num_nodes)]
    headers = ['Düğüm', 'Mesafe', 'Önceki']
    
    # Matplotlib ile tablo
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.axis('off')
    table = ax.table(cellText=data, colLabels=headers, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    
    title = f"Adım {step}"
    if edge:
        title += f" (Kenar {edge[0]}->{edge[1]} tarandı)"
    plt.title(title)
    plt.show()

def bellman_ford():
    graph = get_fixed_graph()
    num_nodes = 4  # Sabit düğüm sayısı
    print("\nTanımlı Graf (Kenar: Ağırlık):")
    for u, v, w in graph:
        print(f"{u} -> {v}: {w}")

    # Grafı görselleştir
    draw_graph(graph, num_nodes)

    # Mesafeler ve önceki düğümler
    distances = [float('inf')] * num_nodes
    distances[0] = 0  # Kaynak düğüm 0
    predecessors = [None] * num_nodes

    # Başlangıç tablosu
    print("\nAdım 0 (Başlangıç):")
    print("Düğüm | Mesafe | Önceki Düğüm")
    print("-" * 30)
    for i in range(num_nodes):
        dist = str(distances[i]) if distances[i] != float('inf') else "∞"
        pred = str(predecessors[i]) if predecessors[i] is not None else "-"
        print(f"{i}     | {dist:>6} | {pred:>12}")
    draw_table(distances, predecessors, step=0)

    # |V|-1 iterasyon
    step = 1
    for i in range(num_nodes - 1):
        updated = False
        for u, v, w in graph:
            if distances[u] != float('inf') and distances[u] + w < distances[v]:
                distances[v] = distances[u] + w
                predecessors[v] = u
                updated = True
                print(f"\nAdım {step} (Kenar {u}->{v} tarandı):")
                print("Düğüm | Mesafe | Önceki Düğüm")
                print("-" * 30)
                for j in range(num_nodes):
                    dist = str(distances[j]) if distances[j] != float('inf') else "∞"
                    pred = str(predecessors[j]) if predecessors[j] is not None else "-"
                    print(f"{j}     | {dist:>6} | {pred:>12}")
                draw_table(distances, predecessors, step=step, edge=(u, v))
                step += 1
            else:
                print(f"\nAdım {step} (Kenar {u}->{v} tarandı, güncelleme yok):")
                print("Düğüm | Mesafe | Önceki Düğüm")
                print("-" * 30)
                for j in range(num_nodes):
                    dist = str(distances[j]) if distances[j] != float('inf') else "∞"
                    pred = str(predecessors[j]) if predecessors[j] is not None else "-"
                    print(f"{j}     | {dist:>6} | {pred:>12}")
                draw_table(distances, predecessors, step=step, edge=(u, v))
                step += 1
        if not updated:
            print(f"\nAdım {step-1}'den sonra değişiklik olmadı. Algoritma erken bitti.")
            break

    # Negatif çevrim kontrolü
    for u, v, w in graph:
        if distances[u] != float('inf') and distances[u] + w < distances[v]:
            print("\nHata: Graf negatif ağırlıklı bir çevrim içeriyor!")
            return None, None, None

    return distances, predecessors, graph

def main():
    distances, predecessors, graph = bellman_ford()
    if distances is None:
        return

    print("\nSonuç:")
    print("Düğüm | En Kısa Mesafe | Önceki Düğüm")
    print("-" * 35)
    for i in range(4):
        dist = str(distances[i]) if distances[i] != float('inf') else "∞"
        pred = str(predecessors[i]) if predecessors[i] is not None else "-"
        print(f"{i}     | {dist:>12} | {pred:>12}")

    print("\nKaynak (0) düğümünden diğer düğümlere en kısa yollar:")
    for i in range(4):
        if distances[i] == float('inf'):
            print(f"Düğüm {i}'e yol yok.")
            continue
        path = []
        current = i
        while current is not None:
            path.append(current)
            current = predecessors[current]
        path.reverse()
        print(f"Düğüm {i}'e yol: {' -> '.join(map(str, path))} (Mesafe: {distances[i]})")

if __name__ == "__main__":
    main()