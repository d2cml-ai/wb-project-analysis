import os
import pinecone
import openai
import Constants
from prompts import router_prompt

openai.api_key = Constants.OPENAI_API_KEY
os.environ["PINECONE_API_KEY"] = Constants.PINECONE_API_KEY
os.environ["PINECONE_ENVIRONMENT"] = Constants.PINECONE_ENVIRONMENT

def constructRouterMessages(userInput):
        messages = [
                {"role": "system", "content": router_prompt},
                {"role": "user", "content": userInput}
        ]
        return messages

def routeQuery(query):
        messages = constructRouterMessages(query)
        routerResponse = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                temperature=0.0
        )
        classification = routerResponse["choices"][0]["message"]["content"]
        return classification

# def main():
#         userInput = ""

#         while userInput != "exit":
#                 userInput = input("Query: ")
#                 messages = constructRouterMessages(userInput)
#                 routerResponse = openai.ChatCompletion.create(
#                         model="gpt-4",
#                         messages=messages,
#                         temperature=0.0
#                 )
#                 classification = routerResponse["choices"][0]["message"]["content"]
#                 print(classification)

# if __name__ == "__main__":
#         main()