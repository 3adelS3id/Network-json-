from flask import Flask, render_template, request
from fastapi import FastAPI
import os
from dotenv import load_dotenv  
import pathlib
import textwrap
import streamlit as st
import google.generativeai as genai
import google.ai.generativelanguage as glm
import PIL.Image


app = FastAPI()

@app.get("/")
def read_root(): 
    return {"Welcome":"Network-Bot"}
load_dotenv()
genai.configure(api_key=os.environ["API_KEY"])
    # Function to load Gemini Pro model and get responce
model = genai.GenerativeModel("gemini-pro")
chat=model.start_chat(history=[])
def get_gemini_responce(prompt):
    responce=chat.send_message(prompt,stream=True)
    responce.resolve()   
    return responce

#intialize our streamlit app 
st.header("Draw a Network Bot")

#initialize session state for chat history if doesny exist 
if 'chat_history' not in st.session_state:
    st.session_state['chat_history']= []

input=st.text_input("You: ",key="input")
submit=st.button("Ask the question ?")

if submit and input:
    responce=get_gemini_responce(input)
    
    ##Add user query and responce to session chat history 
    st.session_state['chat_history'].append(("You :",input))
    st.subheader("The Responce is ")
    for chunk in responce:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot :",chunk.text))
        
# History 
st.subheader("Chat History ")
for role,text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")

