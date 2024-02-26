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



#os.environ['GOOGLE_API_KEY'] = 'D:\2024\project\api\venv\.env'
genai.configure( api_key= 'AIzaSyCruf9GIkS40G0Tjmu1QsA5NS9mDNVEAiY')

# Function to load Gemini Pro model and get responce
model = genai.GenerativeModel('gemini-pro-vision')
def get_gemini_responce(input,image):
    if input!="":
       response = model.generate_content([input,image])
    else:
       response = model.generate_content(image)
       
    return response.text

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
   response=get_gemini_responce(input,image)
   st.subheader("The Responce is ")
   st.write(response)
 #  with open('generate_graph.py', 'w') as file:
 #        responce = str(response)
 #        file.write(response)
  #       print("Script saved as 'generate_graph.py'.")
  #       command = ["generate_graph.py"]
# Execute the command
#         subprocess.run(command)
   
openai.api_key = st.secrets["OPENAI_API_KEY"]'

def chat_completion(messages: list) -> str:
    try:
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages
        )
        return completion['choices'][0]['message']['content']
    except:
        return 'We are facing a technical issue at this moment.'

def generate_messages(messages: list, query: str) -> list:
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
   
   


    

        
