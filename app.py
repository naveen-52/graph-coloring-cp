from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import matplotlib
import networkx as nx
import itertools
import io
import base64
import heapq
from collections import Counter

matplotlib.use('Agg')

app = Flask(__name__)

@app.context_processor
def utility_processor():
    return dict(chr=chr)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/graph-coloring')
def graph_coloring_index():
    return render_template('graph_coloring/index.html')

@app.route('/graph-coloring/matrix', methods=['POST'])
def graph_coloring_matrix():
    num_vertices = int(request.form['num_vertices'])
    return render_template('graph_coloring/matrix.html', num_vertices=num_vertices)

@app.route('/graph-coloring/visualize', methods=['POST'])
def graph_coloring_visualize():
    num_vertices = int(request.form['num_vertices'])
    try:
        matrix = [[int(request.form[f'cell_{i}_{j}']) for j in range(num_vertices)] for i in range(num_vertices)]
    except ValueError:
        return "Invalid input. Please enter integers only."

    G = nx.Graph()
    G.add_nodes_from(range(num_vertices))
    G.add_edges_from((i, j) for i in range(num_vertices) for j in range(num_vertices) if matrix[i][j] == 1)

    labels = {i: chr(65 + i) for i in range(num_vertices)}

    plt.figure(figsize=(6, 6))
    pos = nx.circular_layout(G)
    nx.draw(G, pos, labels=labels, with_labels=True, node_color='skyblue', node_size=700, edge_color='gray', font_color='black')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    graph_url = base64.b64encode(buf.getvalue()).decode('utf8')
    plt.close()

    return render_template('graph_coloring/graph.html', graph_url=graph_url, num_vertices=num_vertices, matrix=matrix)

def welsh_powell_vertex_coloring(G):
    coloring = {}
    nodes_sorted = sorted(G.nodes(), key=lambda node: G.degree(node), reverse=True)
    for node in nodes_sorted:
        used_colors = set(coloring.get(neigh, None) for neigh in G.neighbors(node))
        color = next(color for color in range(len(G)) if color not in used_colors)
        coloring[node] = color
    return coloring

@app.route('/graph-coloring/chromatic', methods=['POST'])
def graph_coloring_chromatic():
    try:
        num_vertices = int(request.form['num_vertices'])
        matrix = [[int(request.form[f'cell_{i}_{j}']) for j in range(num_vertices)] for i in range(num_vertices)]

        G = nx.Graph()
        G.add_nodes_from(range(num_vertices))
        G.add_edges_from((i, j) for i in range(num_vertices) for j in range(num_vertices) if matrix[i][j] == 1)

        vertex_coloring = welsh_powell_vertex_coloring(G)
        chromatic_index = max(vertex_coloring.values()) + 1

        colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'orange', 'purple', 'pink', 'brown']

        pos = nx.circular_layout(G)

        def draw_graph(G, vertex_coloring, color_mapping, num_vertices, pos):
            labels = {i: chr(65 + i) for i in range(num_vertices)}
            plt.figure(figsize=(6, 6))
            node_colors = [color_mapping[vertex_coloring[node]] for node in G.nodes()]
            nx.draw(G, pos, labels=labels, with_labels=True, node_color=node_colors, node_size=700, edge_color='gray', font_color='black')
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plt.close()
            return base64.b64encode(buf.getvalue()).decode('utf8')

        color_combinations = list(itertools.permutations(colors[:chromatic_index]))

        graphs = []
        for color_mapping in color_combinations:
            color_mapping_dict = {i: color for i, color in enumerate(color_mapping)}
            graph_url = draw_graph(G, vertex_coloring, color_mapping_dict, num_vertices, pos)
            graphs.append(graph_url)

        return render_template('graph_coloring/chromatic_index.html', chromatic_index=chromatic_index, graphs=graphs)

    except Exception as e:
        print(f"Error: {e}")
        return str(e)

@app.route('/graph-coloring/manual', methods=['GET'])
def graph_coloring_manual():
    num_vertices = int(request.args['num_vertices'])
    matrix = [[int(request.args[f'cell_{i}_{j}']) for j in range(num_vertices)] for i in range(num_vertices)]
    return render_template('graph_coloring/manual_color.html', num_vertices=num_vertices, matrix=matrix)

@app.route('/graph-coloring/manual-process', methods=['POST'])
def graph_coloring_manual_process():
    try:
        num_vertices = int(request.form['num_vertices'])
        num_colors = int(request.form['num_colors'])
        matrix = [[int(request.form[f'cell_{i}_{j}']) for j in range(num_vertices)] for i in range(num_vertices)]

        G = nx.Graph()
        G.add_nodes_from(range(num_vertices))
        G.add_edges_from((i, j) for i in range(num_vertices) for j in range(num_vertices) if matrix[i][j] == 1)

        vertex_coloring = welsh_powell_vertex_coloring(G)
        colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'orange', 'purple', 'pink', 'brown']

        pos = nx.circular_layout(G)

        def draw_graph(G, vertex_coloring, color_mapping, num_vertices, pos):
            labels = {i: chr(65 + i) for i in range(num_vertices)}
            plt.figure(figsize=(6, 6))
            node_colors = [color_mapping[vertex_coloring[node]] for node in G.nodes()]
            nx.draw(G, pos, labels=labels, with_labels=True, node_color=node_colors, node_size=700, edge_color='gray', font_color='black')
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plt.close()
            return base64.b64encode(buf.getvalue()).decode('utf8')

        color_combinations = []
        for i in range(0, num_colors - num_vertices + 1):
            start_idx = i
            end_idx = start_idx + num_vertices
            color_combinations.extend(itertools.permutations(colors[start_idx:end_idx]))

        graphs = []
        for color_mapping in color_combinations:
            color_mapping_dict = {i: color for i, color in enumerate(color_mapping)}
            graph_url = draw_graph(G, vertex_coloring, color_mapping_dict, num_vertices, pos)
            graphs.append(graph_url)

        return render_template('graph_coloring/manual_color_result.html', graphs=graphs)

    except Exception as e:
        print(f"Error: {e}")
        return str(e)

@app.route('/mst')
def mst_index():
    return render_template('mst/index.html')

@app.route('/mst/matrix', methods=['POST'])
def mst_matrix():
    num_vertices = int(request.form['num_vertices'])
    return render_template('mst/matrix.html', num_vertices=num_vertices)

def prims_mst(num_vertices, matrix):
    visited = [False] * num_vertices
    mst_edges = []
    min_heap = [(0, 0, -1)]
    total_weight = 0

    while min_heap:
        weight, current, parent = heapq.heappop(min_heap)

        if visited[current]:
            continue

        visited[current] = True

        if parent != -1:
            mst_edges.append((parent, current, weight))
            total_weight += weight

        for neighbor in range(num_vertices):
            if not visited[neighbor] and matrix[current][neighbor] > 0:
                heapq.heappush(min_heap, (matrix[current][neighbor], neighbor, current))

    return mst_edges, total_weight

@app.route('/mst/calculate', methods=['POST'])
def mst_calculate():
    try:
        num_vertices = int(request.form['num_vertices'])
        matrix = [[int(request.form[f'cell_{i}_{j}']) for j in range(num_vertices)] for i in range(num_vertices)]

        mst_edges, total_weight = prims_mst(num_vertices, matrix)

        G = nx.Graph()
        G.add_nodes_from(range(num_vertices))
        for i in range(num_vertices):
            for j in range(num_vertices):
                if matrix[i][j] > 0:
                    G.add_edge(i, j, weight=matrix[i][j])

        labels = {i: chr(65 + i) for i in range(num_vertices)}
        edge_labels = {(i, j): matrix[i][j] for i in range(num_vertices) for j in range(num_vertices) if matrix[i][j] > 0}

        plt.figure(figsize=(8, 8))
        pos = nx.circular_layout(G)

        mst_edge_list = [(edge[0], edge[1]) for edge in mst_edges]
        all_edges = list(G.edges())
        non_mst_edges = [edge for edge in all_edges if edge not in mst_edge_list and (edge[1], edge[0]) not in mst_edge_list]

        nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=700)
        nx.draw_networkx_labels(G, pos, labels, font_size=12, font_color='black')
        nx.draw_networkx_edges(G, pos, edgelist=non_mst_edges, edge_color='gray', width=2, style='dashed')
        nx.draw_networkx_edges(G, pos, edgelist=mst_edge_list, edge_color='green', width=4)
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=10)

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        graph_url = base64.b64encode(buf.getvalue()).decode('utf8')
        plt.close()

        return render_template('mst/result.html', graph_url=graph_url, mst_edges=mst_edges, total_weight=total_weight)

    except Exception as e:
        print(f"Error: {e}")
        return str(e)

@app.route('/huffman')
def huffman_index():
    return render_template('huffman/index.html')

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    frequency = Counter(text)
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0] if heap else None

def generate_huffman_codes(root, code="", codes=None):
    if codes is None:
        codes = {}

    if root is None:
        return codes

    if root.char is not None:
        codes[root.char] = code if code else "0"
        return codes

    generate_huffman_codes(root.left, code + "0", codes)
    generate_huffman_codes(root.right, code + "1", codes)

    return codes

@app.route('/huffman/encode', methods=['POST'])
def huffman_encode():
    try:
        text_input = request.form['text_input']

        if not text_input:
            return "Please enter some text."

        frequency = Counter(text_input)
        root = build_huffman_tree(text_input)
        huffman_codes = generate_huffman_codes(root)

        frequencies = sorted(frequency.items(), key=lambda x: x[1], reverse=True)

        original_size = len(text_input) * 8
        compressed_size = sum(len(huffman_codes[char]) * freq for char, freq in frequency.items())
        compression_ratio = round((1 - compressed_size / original_size) * 100, 2) if original_size > 0 else 0

        return render_template('huffman/result.html',
                               original_text=text_input,
                               huffman_codes=huffman_codes,
                               frequencies=frequencies,
                               original_size=original_size,
                               compressed_size=compressed_size,
                               compression_ratio=compression_ratio)

    except Exception as e:
        print(f"Error: {e}")
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
