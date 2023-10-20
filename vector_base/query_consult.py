import openai, pandas as pd
import pinecone, tiktoken
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

import os

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
embeddings =  OpenAIEmbeddings()

pinecone.init()

query = 'conectividad 5g'


vector_database = Pinecone.from_existing_index(
    index_name="wb-projects", 
    embedding=embeddings
)


class Query:
    def __init__(self, query, n=3, model='gpt-3.5-turbo-16k'):
        self.query = query
        self.n = n
        self.model = model

    def query_consult(self):
        retriever = vector_database.\
            as_retriever(search_type="mmr", search_kwargs={'k': self.n})
        docs = retriever.get_relevant_documents(self.query)
        self.docs = docs
        context, data_context = self._get_contexts(docs)

        self.context, self.data_context = context, data_context

    def _get_context(self, doc):
        context = {
            'content': doc.page_content,
            'pdfurl': doc.metadata.get('url')
        }
        return context

    def _get_contexts(self, docs):
        contexts = [
            self._get_context(doc) for doc in docs
        ]
        data_context = pd.DataFrame(contexts)
        return contexts, data_context

    def construct_messages(self, text):
        query = self.query
        
        system_prompt = f'Summarise the following project text in less than 200 words, focusing in the query : {query}'
        user_prompt = f'Relevant context: {text}'
        message = [
            {
                'role': 'system',
                'content': system_prompt
            }, 
            {
                'role': 'user',
                'content': user_prompt
            }
        ]
        return message
    def gpt_response(self, messages):
        response = openai.ChatCompletion.create(
            model=self.model, 
            messages = messages
        )

        result = response['choices'][0]['message']['content']
        return result
    def run_gpt(self):
        texts = self.context
        texts = [x.get('content') for x in texts]
        messages = [
            self.construct_messages(text) for text in texts
        ]
        responses = [
            self.gpt_response(message) for message in messages
        ]
        self.responses = responses