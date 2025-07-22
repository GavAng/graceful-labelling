import networkx as nx
import matplotlib.pyplot as plt


class DirectedChoice:
    def __init__(self):
        G = nx.DiGraph()
        G.add_node(0)
        self.G_left = G.copy()
        self.G_left.add_edge(0, 1)
        self.G_right = G.copy()
        self.G_right.add_edge(1, 0)
        self.x_left = 2
        self.x_right = 1
        self.left_edge_labels = {(0, 1): 1}
        self.right_edge_labels = {(1, 0): 1}

        self.fig, self.axes = plt.subplots(1, 2, figsize=(8, 4))
        self.draw_graphs()

        self.cid = self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        plt.tight_layout()
        plt.show()

    def draw_graphs(self):
        e = len(self.G_left.edges)

        labels_to_edges_left = {
            label: edge for edge, label in self.left_edge_labels.items()
        }
        self.axes[0].cla()
        # self.axes[0].set_title(f"Add edge {labels_to_edges_left[e]}")
        left_layout = nx.spring_layout(self.G_left, k=1.0)
        nx.draw(
            self.G_left,
            pos=left_layout,
            ax=self.axes[0],
            with_labels=True,
            node_color="lightblue",
            arrows=True,
        )
        nx.draw_networkx_edge_labels(
            self.G_left,
            pos=left_layout,
            ax=self.axes[0],
            edge_labels=self.left_edge_labels,
        )

        labels_to_edges_right = {
            label: edge for edge, label in self.right_edge_labels.items()
        }
        self.axes[1].cla()
        # self.axes[1].set_title(f"Add edge {labels_to_edges_right[e]}")
        right_layout = nx.spring_layout(self.G_right, k=1.0)
        nx.draw(
            self.G_right,
            pos=right_layout,
            ax=self.axes[1],
            with_labels=True,
            node_color="lightblue",
            arrows=True,
        )
        nx.draw_networkx_edge_labels(
            self.G_right,
            pos=right_layout,
            ax=self.axes[1],
            edge_labels=self.right_edge_labels,
        )
        self.fig.canvas.draw_idle()

    def on_click(self, event):
        if event.inaxes == self.axes[0]:
            self.G_right = self.G_left.copy()
            self.x_right = self.x_left
        elif event.inaxes == self.axes[1]:
            self.G_left = self.G_right.copy()
            self.x_left = self.x_right

        n = len(self.G_left)

        self.G_left.add_edge(n - self.x_left, n)
        self.x_left += 1

        self.G_right.add_edge(n, self.x_right - 1)

        e = len(self.G_left.edges)

        self.left_edge_labels = {
            edge: (edge[1] - edge[0]) % (e + 1) for edge in self.G_left.edges
        }

        self.right_edge_labels = {
            edge: (edge[1] - edge[0]) % (e + 1) for edge in self.G_right.edges
        }

        self.draw_graphs()


DirectedChoice()
