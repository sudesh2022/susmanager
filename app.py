
import streamlit as st
from openai import OpenAI
import openai
import streamlit as st


openai.api_key = st.secrets.API_KEY

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: lightblue;
    }
</style>
""", unsafe_allow_html=True)


# app sidebar
with st.sidebar:
    st.markdown("""
                # What can I ask ? 
                """)
    with st.expander("Click here to see FAQs"):
        st.info(
            f"""
                - What is corelation between GHD Scope versus total energy consumption ?
                - Do you think energy consumption is increasing linearly with copper production ? 
                - which year water consumption is maximum ?
                - Can you plot a graph of year versus water consumption ?
                - How is the trend for energy consumption with copper production quantity ? 
                - How many years it will take for me to reach net zero GHG Scope 1 based on the trends ?
            """
        )
    st.caption(f"Report bugs to sudesh@sg.ibm.com ")

with st.container():
    col1,col2 = st.columns([8,3])


st.title("Sustainability Manager ")
st.caption("🚀 A streamlit chatbot to answer machine learning findings")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai.api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai.api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)