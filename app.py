import streamlit as st
from openai import OpenAI
import openai
import streamlit as st
import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader
import time


openai.api_key = st.secrets.API_KEY

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: navyblue;
    }
            
            
</style>
""", unsafe_allow_html=True)

st.title("Sustainability Manager Application")

# app sidebar
with st.sidebar:
    st.markdown("""
                # What can I ask ? 
                """)
    with st.expander("Click here to see FAQs"):
        st.info(
            f"""
                - What is SBTi ?
                - What are goals of SBTi 
                - Can you summarize emission accounting requirements ?
                - Which is the G20 country that has the maximum validated target and committed target in 2021 ? 
                - How the GHG emission targets are set by SBTi?
                - What is the difference of 1.5 degree to 2 degree target approach?
                - What approval is needed after finalising the GHG targets?
                - For how many years we can set the GHG targets?
             """
        )
    st.caption(f"Report bugs to sudesh@sg.ibm.com ")

with st.container():
    col1,col2 = st.columns([8,3])

if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "This applicaton uses machine learning findings from Copper mines."}
    ]


@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the docs – hang tight! This should take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        prompt='''
        Please ask question based on the data 
        '''

        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt=prompt))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

index = load_data()


if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question on copper mines"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If the last message is not from the assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            start_time = time.time()  # Record the start time
            response = st.session_state.chat_engine.chat(prompt)
            elapsed_time = time.time() - start_time  # Calculate elapsed time

            # Check if elapsed time is less than 15 seconds
            if elapsed_time < 30:
                st.write(response.response)
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message)
            else:
                st.write("I am sorry, I dont want to keep you waiting. It's not something that I can answer within 15 seconds. Please ask the question in a different manner and I will try to answer within 15 seconds.")
                message = {"role": "assistant", "content": "Custom message for delayed response"}

            #st.session_state.messages.append(message)  # Add response to message history