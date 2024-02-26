import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Create a Graph object
G = nx.Graph()

# Define nodes
nodes = ['Switch in Back Office', 'Switch in Waiting Room', 'Switch in Reception Area',
         'Printer', 'PC in Back Office', 'PCs in Reception Area', 'Wi-Fi Router', 'WAPs',
         'PCs in Suites', 'Cable Modem', 'Firewall', 'Internet']

# Define edges
edges = [('Switch in Back Office', 'Printer'), 
         ('Switch in Back Office', 'PC in Back Office'),
         ('Switch in Back Office', 'Cable Modem'), 
         ('Switch in Back Office', 'Switch in Waiting Room'), 
         ('Switch in Waiting Room', 'Wi-Fi Router'), 
         ('Wi-Fi Router', 'WAPs'), 
         ('WAPs', 'PCs in Suites'), 
         ('Switch in Reception Area', 'PCs in Reception Area'), 
         ('Switch in Reception Area', 'Switch in Back Office'),
         ('Cable Modem', 'Firewall'), 
         ('Firewall', 'Internet')]

# Add nodes and edges to the graph
G.add_nodes_from(nodes)
G.add_edges_from(edges)

# Load images for nodes
img_switch = mpimg.imread('D:/2024/project/api/switch_image.jpg')
img_printer = mpimg.imread('D:/2024/project/api/printer_image.jpg')
img_Router = mpimg.imread('D:/2024/project/api/router_image.jpg')
img_internet = mpimg.imread('D:/2024/project/api/internet_image.jpg')
img_Firewall = mpimg.imread('D:/2024/project/api/firewall_image.jpg')
img_Server = mpimg.imread('D:/2024/project/api/server_image.jpg')
img_pc = mpimg.imread('D:/2024/project/api/pc_image.jpg')

# Draw the graph
pos = nx.spring_layout(G, seed=42)  # positions for all nodes

# Create the figure and axes
fig, ax = plt.subplots(figsize=(12, 8))

# Set background color
fig.patch.set_facecolor('black')
ax.set_facecolor('black')

# Draw nodes with images and labels
node_images = {
    'Switch in Back Office': img_switch,
    'Printer': img_printer,
    'Wi-Fi Router': img_Router,
    'Internet': img_internet,
    'Firewall': img_Firewall,
    'PC in Back Office': img_Server,
    'PCs in Reception Area': img_pc
}

for node, image in node_images.items():
    ax.imshow(image, aspect='auto', extent=(pos[node][0] - 0.1, pos[node][0] + 0.1, 
                                             pos[node][1] - 0.1, pos[node][1] + 0.1))
    ax.text(pos[node][0], pos[node][1] - 0.2, node, ha='center', fontsize=10, color='white')

# Draw edges
nx.draw_networkx_edges(G, pos, ax=ax, edge_color='white')

# Add a title to the graph
plt.title("Network Diagram for the First Floor of the Arborerum Professional Center", color='white')

# Remove axis
ax.set_xticks([])
ax.set_yticks([])

# Show the graph
plt.tight_layout()
plt.show()
