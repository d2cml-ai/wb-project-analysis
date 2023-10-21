import openai
import pinecone
from prompts import project_question_system_prompt, project_question_user_prompt

def contextFromProjectIndexEntry(projectIndexEntry):
        context = ""
        context += f"\n\nProject ID: {projectIndexEntry['id']}\n"
        context += f"URL of Project PDF: {projectIndexEntry['metadata']['url']}\n"
        context += projectIndexEntry["metadata"]["text"]
        return context

def projectQueryResponse(query, projectNumber, pineconeIndex):
        projectIndexEntry = pineconeIndex.query(id=projectNumber)["matches"]
        context = contextFromProjectIndexEntry(projectIndexEntry)
        messages = [
                {"role": "system", "content": project_question_system_prompt},
                {"role": "user", "content": project_question_user_prompt.format(query=query, context=context)}
        ]
        response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                temperature=0.5
        )
        return response["choices"][0]["message"]["content"]

# TODO: add a way to handle several question on the same document without having to specify the id again