import openai
import pinecone
from prompts import project_question_system_prompt, project_question_user_prompt
import Constants
import os

import pandas as pd

database_url = "https://raw.githubusercontent.com/d2cml-ai/wb-project-analysis/database/data/projects_data.csv"
database = pd.read_csv(database_url)


openai.api_key = Constants.OPENAI_API_KEY
os.environ["PINECONE_API_KEY"] = Constants.PINECONE_API_KEY
os.environ["PINECONE_ENVIRONMENT"] = Constants.PINECONE_ENVIRONMENT
# embeddings =  OpenAIEmbeddings()
index_name = "wb-projects"
embeddingModel = "text-embedding-ada-002"
chatModel = "gpt-3.5-turbo-16k"
pinecone.init()
pineconeIndex = pinecone.Index(index_name)
temperature = 0.6


def contextFromProjectIndexEntry(projectIndexEntry):
    context = ""
    context += f"Project ID: {projectIndexEntry['id']}\n"
    context += f"URL of Project PDF: {projectIndexEntry['metadata']['url']}\n"
    context += projectIndexEntry["metadata"]["text"] + "\n\n"
    return context


def projectQueryResponse(info_dict, query, projectNumber, chatModel):
    keys_info = list(info_dict.keys())
    relevant_columns = [x for x in keys_info if x != "query"]
    relevant_data = pd.DataFrame()

    for column in relevant_columns:
        values_col = info_dict.get(column)
        rel_rows_i = database.query(f"{column} in @values_col")
        relevant_data = pd.concat([relevant_data, rel_rows_i])

    #     relevant_data = -0
    print(relevant_data)


#     projectIndexEntry = pineconeIndex.query(
#         id=projectNumber, top_k=1, include_metadata=True
#     )["matches"][0]

#     context = contextFromProjectIndexEntry(projectIndexEntry)
#     messages = [
#         {"role": "system", "content": project_question_system_prompt},
#         {
#             "role": "user",
#             "content": project_question_user_prompt.format(
#                 query=query, context=context
#             ),
#         },
#     ]
#     response = openai.ChatCompletion.create(
#         model=chatModel, messages=messages, temperature=0
#     )
#     return response["choices"][0]["message"]["content"]


# TODO: add a way to handle several question on the same document without having to specify the id again
