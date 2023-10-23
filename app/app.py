import Constants
from project_query import projectQueryResponse
from index_query import getResponseFromQuery
from router import detectQueryType
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
        
        queryRoute = detectQueryType(query)

        if queryRoute:
                st.session_state.response = projectQueryResponse(query, queryRoute, chatModel)
        else:
                st.session_state.response = getResponseFromQuery(query, numberOfResults, chatModel)


def main():
        if "response" not in st.session_state:
                st.session_state.response = ""
        
        if "query" not in st.session_state:
                st.session_state.query = ""
        
        st.write(st.session_state.query)
        st.write(st.session_state.response)

        st.title("WB Projects Analysis Tool")
        st.session_state.chatModel, st.session_state.numberOfResults = sidebarOptions()
        st.text_input(
                "Ask your question here", 
                key = "query",
                placeholder="Are there any projects on 5G connectivity?",
                on_change=generateResponse
        )

if __name__ == "__main__":
        main()
        

# import os
# import streamlit as st

# from vector_base.database import *

# import os, openai
# from dotenv import load_dotenv

# load_dotenv()

# openai.api_key = os.getenv('OPENAI_API_KEY')


# db_ = pd.read_csv('./data/projects_data.csv')

# def convert_df(df):
# 	return df.to_csv(index=False).encode('utf-8')

# csv = convert_df(db_)

# def download_query():
# 	st.sidebar.download_button(
# 		'Download database',
# 		csv, 
# 		'query.csv'
# 	)


# def sidebar():
# 	st.sidebar.title('Configuration')
# 	model = st.sidebar.selectbox(
# 		"Model", ["gpt-3.5-turbo", "gpt-4"]
# 	)
# 	n_query = st.sidebar.number_input(
# 		"Num of queries", 1, 10, 3
# 	)
# 	st.sidebar.title('Download query')

# 	if st.session_state.request:
# 		st.sidebar.selectbox(
# 			'Query', st.session_state.request
# 		)


# 	download_query()
# 	return model, n_query

# def history_var():
# 	if 'query' not in st.session_state:
# 		st.session_state.query = {}
# 	if 'request' not in st.session_state:
# 		st.session_state.request = []
        
# 	return st.session_state.query, st.session_state.request
        
# def run_query(query, n_query):
# 	response = Query(query, n_query)
# 	response.query_consult()
# 	response.run_gpt()
# 	return response
# 	# DataConsult(response).cross_data

# def get_metadata(i, data):
# 	# print(data['projectid', 'repnb', 'pdfurl', 'txturl', 'project_components'])
# 	target = data.iloc[i]
# 	p_id = target['projectid']
# 	r_nb = target['repnb']
# 	txt_id = target['txturl']
# 	pdf_id = target['pdfurl']
# 	text = target['gpt']

# 	info_0 = f"""
# 	Project ID: {p_id}\n | Repnb: {r_nb} | Source: [txt]({txt_id}) | [pdf]({pdf_id})\n
# 	"""

# 	info_1 = f'''
# 	{text}
# 	\n
# 	'''

# 	st.markdown(info_0, unsafe_allow_html=True)
# 	st.markdown(info_1, unsafe_allow_html=True)

# def main():
# 	history, request = history_var()
# 	st.title("WB database - consult")
# 	model, n_query = sidebar()
# 	actual_query = st.text_input(
# 		'Insert Query', key = 'actual_prompt'
# 	)
# 	query_request = st.session_state.actual_prompt
# 	# print(st.session_state)
# 	# # Query

# 	# print(history.keys())
# 	if query_request not in request:
# 		request.append(query_request)
        
# 	if query_request not in list(history.keys()) and query_request != '':
# 		info_cols = ['projectid', 'repnb', 'pdfurl', 'txturl']
# 		show_col = db_[info_cols]
# 		info = run_query(query_request, n_query)
# 		data_with_metadata = info.data_context.merge(show_col, on = 'pdfurl', how='left')
                 
# 		# st.table(data_with_metadata[info_cols])
                
# 		history[query_request] = info.responses
# 		data_with_metadata['gpt'] = info.responses
                
# 		# all_info = [
# 		# 	get_metadata(i, data_with_metadata) for i in range(n_query)
# 		# ]
# 		for i in range(n_query):
# 			get_metadata(i, data_with_metadata)
# 		# print(history)
# 		# get_metadata(0, data_with_metadata)
                
        


# 	# Query

# if __name__ == '__main__':
# 	main()