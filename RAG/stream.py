import streamlit as st
import requests 
from streamlit_lottie import st_lottie
from rag_with_palm import RAGPaLMQuery

rag_palm_query_instance = RAGPaLMQuery(st.session_state)

def load_lottieurl(url):
    r=requests.get(url)
    if r.status_code!=200:
        return None
    return r.json()

lottie_education=load_lottieurl("https://lottie.host/7a1ee71b-371f-4356-a6fd-9f63d3a5eb38/3rCOzceMYr.json")

def main():
    st.title("Welcome to Eddie - Your Educational Website")
    
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ("Chatbot", "Subject", "About Us"))

    if page == "Chatbot":
        st.header("Welcome to Eddie's Home")
        st.write("Here, you can explore various courses and educational materials.")
        if "messages" not in st.session_state:
            st.session_state.messages = []
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        # React to user input
        if prompt := st.chat_input("Need info? Drop your question here!"):
            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            response = rag_palm_query_instance.query_response(prompt)
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(response) 
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

    elif page == "Subject":
        st.header("Explore Courses")
        st.write("Choose a course to start learning!")

        selected_course = st.selectbox("Select a Course", ("Mathematics", "Science", "History", "Programming"))
        
        if selected_course == "Mathematics":
            st.subheader("Mathematics Course")
            st.write("This course covers various topics in Mathematics.")

        # Add similar blocks for other courses (Science, History, Programming) with respective content
        
    elif page == "About Us":
        st.header("About Eddie")
        st.write("Eddie is an educational platform aimed at providing quality learning materials.")
        st.write("Feel free to explore and learn!")

    
with st.sidebar:
    st_lottie(lottie_education, height=300, key="learn")
    
if __name__ == "__main__":
    main()
