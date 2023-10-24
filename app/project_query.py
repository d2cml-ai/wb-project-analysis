import openai
import pinecone
from prompts import project_question_system_prompt, project_question_user_prompt
import Constants
import os

openai.api_key = Constants.OPENAI_API_KEY
os.environ["PINECONE_API_KEY"] = Constants.PINECONE_API_KEY
os.environ["PINECONE_ENVIRONMENT"] = Constants.PINECONE_ENVIRONMENT
# embeddings =  OpenAIEmbeddings()
index_name = "wb-projects"
# embeddingModel = "text-embedding-ada-002"
chatModel = "gpt-3.5-turbo-16k"
pinecone.init()
pineconeIndex = pinecone.Index(index_name)
temperature = 0.6

def getProjectIndexEntry(projectNumber):
        if "PAD" in projectNumber or "PP" in projectNumber or "P" not in projectNumber:
                projectIndexEntry = pineconeIndex.query(
                        filter={"repnb": projectNumber},
                        vector=[0.0] * 1536,
                        top_k=1,
                        include_metadata=True
                )
                return projectIndexEntry["matches"][0]
        projectIndexEntry = pineconeIndex.query(
                id=projectNumber,
                top_k=1,
                include_metadata=True
        )
        return projectIndexEntry["matches"][0]

def contextFromProjectIndexEntry(projectIndexEntry):
        context = ""
        context += f"Project ID: {projectIndexEntry['id']}\n"
        context += f"URL of Project PDF: {projectIndexEntry['metadata']['url']}\n"
        context += projectIndexEntry["metadata"]["text"] + "\n\n"
        return context

def projectQueryResponse(query, projectNumber, chatModel):
        projectIndexEntry = getProjectIndexEntry(projectNumber)
        # projectIndexEntry = pineconeIndex.query(
        #         id=projectNumber, 
        #         top_k=1,
        #         include_metadata=True
        # )["matches"][0]
        context = contextFromProjectIndexEntry(projectIndexEntry)
        messages = [
                {"role": "system", "content": project_question_system_prompt},
                {"role": "user", "content": project_question_user_prompt.format(query=query, context=context)}
        ]
        response = openai.ChatCompletion.create(
                model=chatModel,
                messages=messages,
                temperature=0.5
        )
        return response["choices"][0]["message"]["content"]

# TODO: add a way to handle several question on the same document without having to specify the id again