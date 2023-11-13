import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx
import threading
 
class GraphVisualizationApp(QMainWindow):
    def __init__(self):
        super().__init__()
 
        self.setWindowTitle("Graph Visualization with BFS and DFS")
 
        layout = QVBoxLayout()
 
        self.start_node_input = QLineEdit(self)
        self.start_node_input.setPlaceholderText('Enter start node')
        layout.addWidget(self.start_node_input)
 
        self.target_node_input = QLineEdit(self)
        self.target_node_input.setPlaceholderText('Enter target node')
        layout.addWidget(self.target_node_input)
 
        self.config_label = QLabel('Pause time (seconds):')
        layout.addWidget(self.config_label)
 
        self.pause_time_input = QLineEdit(self)
        self.pause_time_input.setPlaceholderText('Enter pause time')
        self.pause_time_input.setText('0.5')
        layout.addWidget(self.pause_time_input)
 
        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start_search)
        layout.addWidget(self.start_button)
 
        self.bfs_time_label = QLabel('BFS Time: 0.0 seconds')
        layout.addWidget(self.bfs_time_label)
        self.bfs_queue = QLabel('BFS queue : []')
        layout.addWidget(self.bfs_queue)
        self.bfs_path_label = QLabel('BFS path : []')
        layout.addWidget(self.bfs_path_label)
       
        self.dfs_time_label = QLabel('DFS Time: 0.0 seconds')
        layout.addWidget(self.dfs_time_label)
        self.dfs_stack = QLabel('DFS stack : []')
        layout.addWidget(self.dfs_stack)
        self.dfs_path_label = QLabel('DFS path : []')
        layout.addWidget(self.dfs_path_label)
       
        self.bfs_fig, self.bfs_ax = plt.subplots()
        self.dfs_fig, self.dfs_ax = plt.subplots()
 
        self.bfs_canvas = FigureCanvas(self.bfs_fig)
        self.dfs_canvas = FigureCanvas(self.dfs_fig)
 
        self.pause_time = 0.5
        self.graph_pos = None
 
        layout.addWidget(self.bfs_canvas)
        layout.addWidget(self.dfs_canvas)
 
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
 
        self.graph = {
            'S0': ['S1', 'S2', 'S3', 'S4', 'S5'],
            'S1': ['S6', 'S7', 'S8', 'S9'],
            'S2': [],
            'S3': [],
            'S4': [],
            'S5': [],
            'S6': [],
            'S7': [],
            'S8': [],
            'S9': []
        }
        self.G = nx.Graph(self.graph)
 
        self.initial_draw_graph()
 
    def initial_draw_graph(self):
        self.graph_pos = nx.spring_layout(self.G)
        self.update_canvas(self.bfs_canvas, self.bfs_ax, set(), 'BFS - Initial State')
        self.update_canvas(self.dfs_canvas, self.dfs_ax, set(), 'DFS - Initial State')
 
 
    def start_search(self):
        self.bfs_time_label.setText('BFS Time: 0.0 seconds')
        self.dfs_time_label.setText('DFS Time: 0.0 seconds')
        self.bfs_path_label.setText('BFS path : []')
        self.dfs_path_label.setText('DFS path : []')
        self.dfs_stack.setText('DFS stack : []')
        self.bfs_queue.setText('BFS queue : []')
 
        start_node = self.start_node_input.text()
        target_node = self.target_node_input.text()
        self.pause_time = float(self.pause_time_input.text())
 
        threading.Thread(target=self.run_bfs, args=(start_node, target_node), daemon=True).start()
        threading.Thread(target=self.run_dfs, args=(start_node, target_node), daemon=True).start()
 
    def run_bfs(self, start, target):
        start_time = time.time()
        self.bfs(start, target)
        end_time = time.time()
        self.bfs_time_label.setText(f'BFS Time: {end_time - start_time:.2f} seconds')
 
    def run_dfs(self, start, target):
        start_time = time.time()
        self.dfs(start, target)
        end_time = time.time()
        self.dfs_time_label.setText(f'DFS Time: {end_time - start_time:.2f} seconds')
 
    def bfs(self, start, target):
        queue = [start]
        visited = set()
        path = []
 
        while queue:
            self.bfs_queue.setText(f'BFS queue : {queue}')
            node = queue.pop(0)
            self.bfs_queue.setText(f'BFS queue : {queue}')
            visited.add(node)
            path.append(node)
            self.update_canvas(self.bfs_canvas, self.bfs_ax, visited, 'BFS')
            if node == target:
                self.bfs_path_label.setText(f'BFS path : {path}')
                break
            for n in self.graph[node]:
                if n not in visited:
                    queue.append(n)
                    self.bfs_queue.setText(f'BFS queue : {queue}')
 
            time.sleep(self.pause_time)
   
    def dfs(self, start, target):
        stack = [start]
        visited = set()
        path = []
 
        while stack:
            self.dfs_stack.setText(f'DFS stack : {stack}')
            node = stack.pop()
            self.dfs_stack.setText(f'DFS stack : {stack}')
            visited.add(node)
            path.append(node)
            self.update_canvas(self.dfs_canvas, self.dfs_ax, visited, 'DFS')
            if node == target:
                self.dfs_path_label.setText(f'DFS path : {path}')
                break
            for n in self.graph[node]:
                if n not in visited:
                    stack.append(n)
                    self.dfs_stack.setText(f'DFS stack : {stack}')
            time.sleep(self.pause_time)
 
    def update_canvas(self, canvas, ax, visited, title):
        ax.clear()
        ax.set_title(title)
        node_colors = ['red' if node in visited else 'lightblue' for node in self.G]
        nx.draw(self.G, self.graph_pos, ax=ax, with_labels=True, node_color=node_colors)
        canvas.draw()
        QApplication.processEvents()
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = GraphVisualizationApp()
    mainWin.show()
    sys.exit(app.exec_())