import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv


load_dotenv()

## langsmith tracking

os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_PROJECT'] = 'Simple q&a chatbot with OPENAI'

### prompt template

prompt = ChatPromptTemplate.from_messages(

    [
        ('system','You are helpful assistant. please response to user queries'),
        ('user','question:{question}')
    ]
)

def generate_response(question,api_key,engine,temperature,max_tokens):
    openai.api = api_key
    llm = ChatOpenAI(model=engine)
    output = StrOutputParser()
    chain = prompt | llm | output
    answer = chain.invoke({'question':question})
    return answer

## stramlit 

st.title('Q and A chatbot')

##sidebar
api_key = st.sidebar.text_input('Give your Open AI API key',type='password')

engine = st.sidebar.selectbox('Select an Open AI model',["gpt-4o","gpt-4-turbo","gpt-4"])

temperature = st.sidebar.slider("Temperatur",min_value=0.0,max_value=1.0,value=0.7)

max_tokens = st.sidebar.slider("Max_Tokens",min_value=50,max_value=300,value=150)


## user input

st.write("Ask Any Question")

user_input = st.text_input("Ask:")

if user_input and api_key:
    response = generate_response(user_input,api_key,engine,temperature,max_tokens)
    st.write(response)
elif user_input:
    st.warning("Please provide API Key")
else:
    st.warning("please ask any queries")






