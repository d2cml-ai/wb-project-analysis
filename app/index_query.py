import openai
import pinecone
import Constants
# from langchain.embeddings import OpenAIEmbeddings
import os
from prompts import project_question_user_prompt, project_question_system_prompt

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

def getTextsAndMetadata(relevantProjects: list[dict]):
        projectTextsAndMetadata = []
        
        for project in relevantProjects:
                projectTextsAndMetadata += [{
                        "id": project["id"],
                        "text": project["metadata"]["text"],
                        "url": project["metadata"]["url"]
                }]
        
        return projectTextsAndMetadata

# def getContextFromQueryResults(relevantProjects):
#         context = ""
#         projectTextsAndMetadata = getTextsAndMetadata(relevantProjects)
        
#         for index, projectInfo in enumerate(projectTextsAndMetadata):
#                 context += f"Text #{index + 1}\n"
#                 context += f"Project ID: {projectInfo['id']}\n"
#                 context += f"URL to project PDF: {projectInfo['url']}\n"
#                 context += f"Project Text:\n{projectInfo['text']}\n\n"
        
#         return context

def buildMessages(query, project):
        messages = [
                {"role": "system", "content": project_question_system_prompt},
                {"role": "user", "content": project_question_user_prompt.format(query=query, context=project["text"])}
        ]
        return messages

def getResponseForProject(query, project, chatModel):
        messages = buildMessages(query, project)
        apiResponse = openai.ChatCompletion.create(
                messages=messages,
                temperature=temperature,
                model=chatModel
        )
        response = apiResponse["choices"][0]["message"]["content"]
        parsedResponse = f"Project ID: {project['id']}\n\nURL for project PDF: {project['url']}\n\nResponse:\n{response}\n\n\n\n"
        return parsedResponse

def getIndependentResponses(query, relevantProjects, chatModel):
        independentResponses = []
        textsAndMetadata = getTextsAndMetadata(relevantProjects)

        for project in textsAndMetadata:
                independentResponses += [{"response": getResponseForProject(query, project, chatModel), "context": project}]
        
        return independentResponses

def getResponseFromQuery(query, numberOfResults, chatModel):
        embeddedQuery = openai.Embedding.create(
                model=embeddingModel,
                input=query,
                encoding_format="float"
        )
        # embeddedQuery = embeddings.embed_query(query)
        relevantProjects = pineconeIndex.query(
                embeddedQuery["data"][0]["embedding"],
                top_k=numberOfResults,
                include_metadata=True
        )["matches"]
        independentResponses = getIndependentResponses(query, relevantProjects, chatModel)
        parsedResponses = ""

        for response in independentResponses:
                parsedResponses += response["response"]
        
        return parsedResponses