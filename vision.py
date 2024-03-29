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


openai.api_key = os.environ["OPENAI_API_KEY"]
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
                "Ensure to cover all details in this image, like where the devices is and return it in json format!\n" +
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
def chat_completion(messages: list) -> str:
    try:
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            temperature=0,
        )
        return completion['choices'][0]['message']['content']
    except:
        return 'We are facing a technical issue at this moment.'

def generate_messages(messages: list[str], query: str) -> list:
    formated_messages = [
        {
            'role': 'system',
            'content': 'You are a helpful Network Design assistant.'
        }
    ]

    for m in messages:
        formated_messages.append({
            'role': 'user',
            'content': m[0]
        })
        formated_messages.append({
            'role': 'assistant',
            'content': m[1]
        })
    formated_messages.append(
        {
            'role': 'user',
            'content': query
        }
    )
    return formated_messages

def generate_response(query: str, chat_history2: list) -> tuple:
        messages = generate_messages(chat_history2, query)
        bot_message = chat_completion(messages)
        chat_history2.append((query, bot_message))
        time.sleep(random.randint(0, 5))
        return '',chat_history2

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
        response: str =get_gemini_responce(input,image)
        print(response[8:-3].lstrip().rstrip())
        st.subheader("The Responce is ")
        graph_nodes = json.loads(response[8:-3].lstrip().rstrip())
        
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
            if device["id"].lower().find("pc") != -1:
                node_images[device["id"]] = img_pc
                
        for node, image in node_images.items():
            ax.imshow(image, aspect='auto', extent=(pos[node][0] - 0.1, pos[node][0] + 0.1, 
                                                    pos[node][1] - 0.1, pos[node][1] + 0.1))
            ax.text(pos[node][0], pos[node][1] - 0.2, node, ha='center', fontsize=10, color='white')

        # Draw edges
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color='white')
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
