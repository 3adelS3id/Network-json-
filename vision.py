import json
import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import google.ai.generativelanguage as glm
from PIL import Image
import subprocess
import openai
import random
import time
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import io


load_dotenv()

genai.configure(api_key=os.environ["API_KEY"])

# Function to load Gemini Pro model and get responce
model = genai.GenerativeModel('gemini-pro-vision')
def get_gemini_responce(input,image):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    if input!="":
       response = model.generate_content({
           'role': "user",
            'parts': [
                {
                    'text':  "Giving a picture of a floor plan, draw a network digram for this image by using real devices like routers, switches, computers and servers.\n" +
                "\n" +
                "draw network diagram by using this steps as standard for drawing ,Task: Network Drawing Instruction Please follow these steps to draw the network:1-Office Connections: office (the number of offices will be determined later by the user) connects to a switch device.2-Switch Connections:All switches are connected to one switch server.3-Server Connections:The switch server connects to:One router device.Two server device.4-router device connects to : One firewall.5-firewall device connects to : The internet.6-Return Format:Please ensure the network diagram is represented in JSON format." +
                "\n" +
                '''The json file should be in the following format {"devices": [{"id": "device-name", "type": "device-type", "location": "device-location", "connections": [{"id": "device-connected-to-name" }]}]}, Make sure to follow this format only''',
            },
                {
                    "text": input
                },
                {
                    'inline_data': {
                        'data': img_byte_arr,
                        'mime_type': "image/jpeg"
                    },
                }
            ]
        }, generation_config={
           'temperature': 0
       })
    else:
       response = model.generate_content(image)

    return response.text
    
if __name__ == "__main__":
    #intialize our streamlit app
    st.header("Draw a Network Bot")
    input=st.text_input("Input Promot : ",key="input")

    uploaded_file=st.file_uploader("Choose an Image.....",type=["jpg","jpeg","png"])
    image=""
    if uploaded_file is not None :
        image=Image.open(uploaded_file)
        st.image(image,caption="Uploaded Image", use_column_width=True)

    submit=st.button("Descripe this image ?")

    if submit:
        response: str = get_gemini_responce(input, image)
        json_start = response.find('{')
        json_end = response.rfind('}') + 2
        json_str = response[json_start:json_end]
        graph_nodes = json.loads(json_str)
        print(json_str)
        st.subheader("The Responce is ")
        st.json(json_str)
        
        
        # Save JSON code to a file
        with open("network_diagram.json", "w") as json_file:
            json_file.write(json_str)
        st.success("JSON code saved to 'network_diagram.json'")
        G = nx.Graph()
        devices = graph_nodes["devices"]
        nodes = []
        edges = []
        for device in devices:
            nodes.append(device["id"])
            
        for device in devices:
            try:
                for connection in device["connections"]:
                    edges.append((device["id"], connection["id"]))
            except Exception:
               pass
     
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        
        # Load images for nodes
        img_switch = mpimg.imread(r'C:\Users\GREEN STORE\Downloads\Network-json--master\switch_image.jpg')
        img_printer = mpimg.imread(r'C:\Users\GREEN STORE\Downloads\Network-json--master\printer_image.jpg')
        img_Router = mpimg.imread(r'C:\Users\GREEN STORE\Downloads\Network-json--master\router_image.jpg')
        img_internet = mpimg.imread(r'C:\Users\GREEN STORE\Downloads\Network-json--master\internet.jpeg')
        img_Firewall = mpimg.imread(r'C:\Users\GREEN STORE\Downloads\Network-json--master\firewall_image.jpeg')
        img_Server = mpimg.imread(r'C:\Users\GREEN STORE\Downloads\Network-json--master\server_image.jpg')
        img_pc = mpimg.imread(r'C:\Users\GREEN STORE\Downloads\Network-json--master\pc_image.jpg')
         
      # Draw the graph
        pos = nx.spring_layout(G, seed=42)  # positions for all nodes

# Create the figure and axes
        fig, ax = plt.subplots(figsize=(12, 8))

# Set background color
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')

# Draw nodes with images and labels
        node_images = {}
        for device in devices:
            match device["type"].lower():
                case "router":
                    node_images[device["id"]] = img_Router
                case "switch":
                    node_images[device["id"]] = img_switch
                case "server":
                    node_images[device["id"]] = img_Server
                case "pc" | "computer":
                    node_images[device["id"]] = img_pc
                case "firewall" | "firewall device":
                    node_images[device["id"]] = img_Firewall
                case "internet" | "cloud":
                    node_images[device["id"]] = img_internet
                case "printer" :
                    node_images[device["id"]] = img_printer                
            if device["id"].lower().find("pc") != -1:
                node_images[device["id"]] = img_pc

        for node, image in node_images.items():
            ax.imshow(image, aspect='auto', extent=(pos[node][0] - 0.1, pos[node][0] + 0.1, 
                                                    pos[node][1] - 0.1, pos[node][1] + 0.1))
            ax.text(pos[node][0], pos[node][1] - 0.2, node, ha='center', fontsize=10, color='black')  # Changed text color to black

        # Draw edges
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color='black')  # Changed edge color to black

        # Draw inside box for each group of devices
        for subgraph in nx.connected_components(G):
            if len(subgraph) > 1:
                min_x = min(pos[node][0] for node in subgraph)
                max_x = max(pos[node][0] for node in subgraph)
                min_y = min(pos[node][1] for node in subgraph)
                max_y = max(pos[node][1] for node in subgraph)
                ax.add_patch(plt.Rectangle((min_x - 0.1, min_y - 0.1), max_x - min_x + 0.2, max_y - min_y + 0.2, fill=False, edgecolor='black'))  # Added rectangle patch

        # Remove axis
        ax.set_xticks([])
        ax.set_yticks([])

        # Show the graph
        plt.savefig('network_graph.png')
        plt.tight_layout()
        plt.close(fig)
        Image.open('network_graph.png')

        st.image('network_graph.png')

        
        # with open('generate_graph.py', 'w') as file:
        #    responce = str(response)
        #    file.write(response)
        #    print("Script saved as 'generate_graph.py'.")
        #    command = ["generate_graph.py"]

        #    subprocess.run(command)
