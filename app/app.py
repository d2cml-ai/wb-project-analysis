import Constants
from project_query import projectQueryResponse
from index_query import getResponseFromQuery
from router import detectDocumentQuery
import streamlit as st

def sidebarOptions():
        st.sidebar.title("Settings")
        chatModel = st.sidebar.selectbox(
                "Select Language Model: ",
                ["gpt-3.5-turbo-16k", "gpt-4"]
        )
        numberOfResults = st.sidebar.number_input("Number of documents: ", 1, 10, 3)
        return chatModel, numberOfResults

def generateResponse():
        query = st.session_state.query
        chatModel = st.session_state.chatModel
        numberOfResults = st.session_state.numberOfResults

        if query == "":
                return
        
        queryRoute = detectDocumentQuery(query)

        if queryRoute:
                st.session_state.response = projectQueryResponse(query, queryRoute, chatModel)
        else:
                st.session_state.response = getResponseFromQuery(query, numberOfResults, chatModel)


def main():
        if "response" not in st.session_state:
                st.session_state.response = ""
        
        if "query" not in st.session_state:
                st.session_state.query = ""
        
        st.title("WB Projects Analysis Tool")
        
        st.write(st.session_state.query)
        st.write(st.session_state.response)

        st.session_state.chatModel, st.session_state.numberOfResults = sidebarOptions()
        st.text_input(
                "Ask your question here", 
                key = "query",
                placeholder="Are there any projects on 5G connectivity?",
                on_change=generateResponse
        )

if __name__ == "__main__":
        main()