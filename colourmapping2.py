import tkinter as tk
from tkinter import messagebox, Canvas, ttk, colorchooser
import math
import random

# Graph coloring logic
def is_safe(graph, node, color, coloring):
    for neighbor in graph[node]:
        if neighbor in coloring and coloring[neighbor] == color:
            return False
    return True

def color_graph(graph, num_colors):
    coloring = {}

    def solve(node):
        if node == len(graph):
            return True
        for color in range(num_colors):
            if is_safe(graph, node, color, coloring):
                coloring[node] = color
                if solve(node + 1):
                    return True
                del coloring[node]
        return False

    return coloring if solve(0) else None

# Default colors
PREDEFINED_COLORS = [
    "#ff5733", "#33ff57", "#3357ff", "#ff33a1", "#a133ff",
    "#33fff5", "#f5ff33", "#ff8c33", "#8c33ff", "#33ff8c"
]

USER_COLORS = []

def pick_colors():
    global USER_COLORS
    USER_COLORS = []
    try:
        n = int(num_colors_entry.get())
        for i in range(n):
            color = colorchooser.askcolor(title=f"Choose color {i+1}")[1]
            if color:
                USER_COLORS.append(color)
    except ValueError:
        messagebox.showerror("Input Error", "Enter a valid number of colors before selecting.")

def generate_edges(num_nodes, graph_type):
    edges = []
    if graph_type == "Complete":
        for i in range(num_nodes):
            for j in range(i+1, num_nodes):
                edges.append((i, j))
    elif graph_type == "Cycle":
        for i in range(num_nodes):
            edges.append((i, (i+1)%num_nodes))
    elif graph_type == "Random":
        for i in range(num_nodes):
            for j in range(i+1, num_nodes):
                if random.random() < 0.4:
                    edges.append((i, j))
    return edges

def solve_graph():
    try:
        num_nodes = int(num_nodes_entry.get())
        num_colors = int(num_colors_entry.get())
        graph_type = graph_type_var.get()
        edges_text = edges_entry.get().strip()

        graph = {i: [] for i in range(num_nodes)}
        edges = []

        if graph_type == "Manual":
            if edges_text:
                try:
                    edges = [tuple(map(int, pair.split(','))) for pair in edges_text.split(';')]
                except Exception:
                    raise ValueError("Invalid edge format.")
            else:
                raise ValueError("Manual mode selected but no edges entered.")
        else:
            edges = generate_edges(num_nodes, graph_type)
            edges_entry.delete(0, tk.END)
            edges_entry.insert(0, ";".join([f"{u},{v}" for u, v in edges]))

        for u, v in edges:
            if u < 0 or v < 0 or u >= num_nodes or v >= num_nodes:
                raise ValueError("Edge contains node outside valid range.")
            graph[u].append(v)
            graph[v].append(u)

        coloring = color_graph(graph, num_colors)
        if coloring:
            draw_graph(graph, coloring)

            for widget in color_mapping_frame.winfo_children():
                widget.destroy()

            color_mapping_frame.pack(pady=10, fill=tk.X, padx=20)
            tk.Label(color_mapping_frame, text="Color Mapping:", font=("Arial", 12, "bold"), bg="#34495e", fg="white").pack(anchor="w", pady=5)

            all_colors = USER_COLORS if USER_COLORS else PREDEFINED_COLORS
            for node, color_index in coloring.items():
                color_name = all_colors[color_index % len(all_colors)]
                row_frame = tk.Frame(color_mapping_frame, bg="#34495e")
                row_frame.pack(anchor="w", pady=2)
                tk.Label(row_frame, text=f"Node {node}:", font=("Arial", 12), bg="#34495e", fg="white").pack(side="left", padx=5)
                tk.Label(row_frame, bg=color_name, width=15, height=1).pack(side="left")

        else:
            messagebox.showinfo("Result", "No valid coloring found.")
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

def draw_graph(graph, coloring):
    canvas.delete("all")
    num_nodes = len(graph)
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    padding = 60
    max_radius = min(canvas_width, canvas_height) // 2 - padding
    node_radius = max(20, min(40, max_radius // max(1, num_nodes)))

    center_x = canvas_width // 2
    center_y = canvas_height // 2
    angle_step = 360 / max(1, num_nodes)
    node_coords = {}

    for i in range(num_nodes):
        angle = i * angle_step
        x = center_x + max_radius * math.cos(math.radians(angle))
        y = center_y + max_radius * math.sin(math.radians(angle))
        node_coords[i] = (x, y)

    for u, neighbors in graph.items():
        x1, y1 = node_coords[u]
        for v in neighbors:
            if u < v:
                x2, y2 = node_coords[v]
                canvas.create_line(x1, y1, x2, y2, width=2, fill="#aaa")

    all_colors = USER_COLORS if USER_COLORS else PREDEFINED_COLORS
    for node, (x, y) in node_coords.items():
        color_index = coloring[node]
        fill_color = all_colors[color_index % len(all_colors)]
        canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius,
                           fill=fill_color, outline="black", width=2)
        canvas.create_text(x, y, text=str(node), fill="white", font=("Arial", 12, "bold"))

# GUI Setup
root = tk.Tk()
root.title("Graph Coloring Tool")
root.geometry("1050x720")
root.configure(bg="#2c3e50")

title_label = tk.Label(root, text="Graph Coloring Tool", font=("Helvetica", 24, "bold"), bg="#2c3e50", fg="white")
title_label.pack(pady=10)

input_frame = tk.Frame(root, bg="#34495e", padx=20, pady=15)
input_frame.pack(pady=10, fill=tk.X, padx=20)

# Inputs
tk.Label(input_frame, text="Nodes:", font=("Arial", 12), bg="#34495e", fg="white").grid(row=0, column=0, padx=10, pady=5)
num_nodes_entry = ttk.Entry(input_frame, width=10)
num_nodes_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(input_frame, text="Colors:", font=("Arial", 12), bg="#34495e", fg="white").grid(row=0, column=2, padx=10, pady=5)
num_colors_entry = ttk.Entry(input_frame, width=10)
num_colors_entry.grid(row=0, column=3, padx=10, pady=5)

tk.Label(input_frame, text="Graph Type:", font=("Arial", 12), bg="#34495e", fg="white").grid(row=1, column=0, padx=10, pady=5)
graph_type_var = tk.StringVar(value="Manual")
ttk.Combobox(input_frame, textvariable=graph_type_var, values=["Manual", "Complete", "Cycle", "Random"], width=15, state="readonly").grid(row=1, column=1, padx=10)

tk.Label(input_frame, text="Edges (u,v;...):", font=("Arial", 12), bg="#34495e", fg="white").grid(row=2, column=0, padx=10, pady=5)
edges_entry = ttk.Entry(input_frame, width=50)
edges_entry.grid(row=2, column=1, columnspan=3, padx=10, pady=5)

# Buttons
tk.Button(input_frame, text="Choose Colors", command=pick_colors, bg="#27ae60", fg="white").grid(row=3, column=0, columnspan=2, pady=5)
solve_button = ttk.Button(input_frame, text="Solve Graph", command=solve_graph)
solve_button.grid(row=3, column=2, columnspan=2, pady=5)

# Canvas
canvas_frame = tk.Frame(root, bg="#2c3e50", padx=10, pady=10)
canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
canvas = Canvas(canvas_frame, bg="#222")
canvas.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

# Mapping display
color_mapping_frame = tk.Frame(root, bg="#34495e", padx=10, pady=10)
color_mapping_frame.pack_forget()

def resize_canvas(event):
    canvas.config(width=event.width, height=event.height)

canvas.bind("<Configure>", resize_canvas)

root.mainloop()

