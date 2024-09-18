import streamlit as st
import random
import os
import openai
from PIL import Image

logo = Image.open("wbg-logo.png")

st.set_page_config(page_title="Assistant", initial_sidebar_state="auto" , page_icon=logo)
st.sidebar.image(logo)
st.sidebar.title("Welcome to your personal AI Assistant")
st.sidebar.divider()
st.sidebar.subheader("How can I help you today?")

openai.api_type = st.secrets["TYPE"]
openai.api_base = st.secrets["BASE"]
openai.api_version = st.secrets["VERSION"]
openai.api_key = st.secrets["KEY"]


conversation = [

    {"role": "system", "content": "You are an AI assistant built to answer the user's questions about World Bank Group (WBG), the "
     "international financial institution that provides loans and grants to the governments of low- and middle-income countries for the purpose of pursuing capital projects. "
     "Their website is https://scorecard.worldbank.org/en/scorecard/home. Feel free to access any data available there. "
     "There is a lot of information and data provided on that URL, try and answer any relevant questions based on data from that website. "
     "You will help people find relevant information about the organisation as well as their efforts with the scorecard. "
     "Do not respond to questions about topics or domains other than World Bank Group's area of operation or efforts. "
     "If asked about other topics or competitors, mention that you are an assistant for WBG, and are only programmed "
     "to answer questions about their domain or provide information about the organisation, its products and its operations."
     "If asked questions about competitor brands, do not provide any information about them. Instead mention that you are "
     "an assistant for WBG, and ask if you can provide any information about them."
    
    }
    
    
    
    
    # {"role": "user", "content": "what are the coffee types?"},
    # {"role": "assistant", "content": "There are various types of coffee, including hot coffees, iced coffees, "
    #                                  "hot teas, iced teas, and more. Some examples of hot coffees are Caribou Coffee "
    #                                  "S'mores Cabin Latte, and Lavender Latte. Some examples of iced coffees are "
    #                                  " McCafe Iced One Step Mocha "
    #                                  "Frappe and Iced Caramel Cookie Coffee. Hot tea options include Mother Rose "
    #                                  "Best and English Breakfast Latte. Iced tea options include Iced Bubble Tea Latte."
    #                                  " Additionally, there are various desserts and more, such as Athletic Brew Co "
    #                                  "Free Wave Hazy IPA Iced Coffee and Swiss Miss S'mores Hot Cocoa."},
    # {"role": "user", "content": "what type of caramel coffees are there?"},
    # {"role": "assistant", "content": "There are several types of caramel coffees available, including Caramel Cookie "
    #                                  "Coffee, Caramel Macchiato, and Iced Caramel Cookie Coffee."}
]


if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you today?"}]

for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message(message["role"]): #, avatar=logo):
            st.write(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.write(message["content"])

prompt = st.chat_input("Say something")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    conversation.append({"role": "user", "content": prompt})

    thinking_msg = st.empty()
    thinking_msg.text("Thinking...")

    completion = openai.ChatCompletion.create(
        engine="gpt-35-turbo",
        messages=conversation,
        temperature=0,
        max_tokens=800,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    chat_response = completion.choices[0].message.content

    thinking_msg.empty()
    with st.chat_message("Assistant"): #, avatar=logo):
        st.write(chat_response)

    message = {"role": "assistant", "content": chat_response}
    conversation.append(message)
    st.session_state.messages.append(message)
