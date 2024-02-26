import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Create a Graph object
G = nx.Graph()

# Define nodes and edges based on the provided details
nodes = [
    'Office 1', 'Office 2', 'Office 3', 'Office 4', 'Office 5', 'Office 6',
    'Office 7', 'Office 8', 'Office 9', 'Office 10', 'Switch 1', 'Switch 2',
    'Switch 3', 'Switch 4', 'Switch 5', 'Router 1', 'Firewall 1', 'Server 1',
    'Printer 1', 'Printer 2', 'Printer 3', 'Printer 4', 'Printer 5', 'Printer 6',
    'Printer 7', 'Printer 8', 'Printer 9', 'Printer 10'
]

edges = [
    ('Office 1', 'Switch 1'), ('Office 2', 'Switch 1'),
    ('Office 3', 'Switch 2'), ('Office 4', 'Switch 2'),
    ('Office 5', 'Switch 3'), ('Office 6', 'Switch 3'),
    ('Office 7', 'Switch 4'), ('Office 8', 'Switch 4'),
    ('Office 9', 'Switch 5'), ('Office 10', 'Switch 5'),
    ('Switch 1', 'Router 1'), ('Switch 2', 'Router 1'),
    ('Switch 3', 'Router 1'), ('Switch 4', 'Router 1'),
    ('Switch 5', 'Router 1'), ('Router 1', 'Firewall 1'),
    ('Firewall 1', 'Server 1'),
    ('Switch 1', 'Printer 1'), ('Switch 1', 'Printer 2'),
    ('Switch 2', 'Printer 3'), ('Switch 2', 'Printer 4'),
    ('Switch 3', 'Printer 5'), ('Switch 3', 'Printer 6'),
    ('Switch 4', 'Printer 7'), ('Switch 4', 'Printer 8'),
    ('Switch 5', 'Printer 9'), ('Switch 5', 'Printer 10')
]

# Add nodes and edges to the graph
G.add_nodes_from(nodes)
G.add_edges_from(edges)

# Load images for nodes
img_office = mpimg.imread('pc_image.jpg')
img_switch = mpimg.imread('switch_image.jpg')
img_router = mpimg.imread('router_image.jpg')
img_firewall = mpimg.imread('firewall_image.jpg')
img_server = mpimg.imread('server_image.jpg')
img_printer = mpimg.imread('printer_image.jpg')

# Draw the network diagram
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)

# Draw nodes with images and labels
node_images = {
    'Office 1': img_office, 'Office 2': img_office, 'Office 3': img_office,
    'Office 4': img_office, 'Office 5': img_office, 'Office 6': img_office,
    'Office 7': img_office, 'Office 8': img_office, 'Office 9': img_office,
    'Office 10': img_office, 'Switch 1': img_switch, 'Switch 2': img_switch,
    'Switch 3': img_switch, 'Switch 4': img_switch, 'Switch 5': img_switch,
    'Router 1': img_router, 'Firewall 1': img_firewall, 'Server 1': img_server,
    'Printer 1': img_printer, 'Printer 2': img_printer, 'Printer 3': img_printer,
    'Printer 4': img_printer, 'Printer 5': img_printer, 'Printer 6': img_printer,
    'Printer 7': img_printer, 'Printer 8': img_printer, 'Printer 9': img_printer,
    'Printer 10': img_printer
}

for node, image in node_images.items():
    plt.imshow(image, aspect='auto', extent=(pos[node][0] - 0.1, pos[node][0] + 0.1,
                                             pos[node][1] - 0.1, pos[node][1] + 0.1))
    plt.text(pos[node][0], pos[node][1] - 0.2, node, ha='center', fontsize=10, color='black')

# Draw edges
nx.draw_networkx_edges(G, pos, edge_color='black')

# Set background color
plt.gca().set_facecolor('lightgray')

# Remove axis
plt.axis('off')

# Add a title to the graph
plt.title('Network Diagram', fontsize=14, color='black')

# Show the network diagram
plt.tight_layout()
plt.show()
