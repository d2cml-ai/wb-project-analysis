import os
from langchain.chat_models import ChatOpenAI

from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate

from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv


class Intention(BaseModel):
    query: list = Field(description="Question, intention of the question")
    repnb: list = Field(description="code repnb of the project, or Report No")
    projectid: list = Field(description="project id of the project, or projectid")


load_dotenv()

OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

PROMPT_INFO = """
extract the information from the following {query}.
{format_instructions}
"""

parser = PydanticOutputParser(pydantic_object=Intention)
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model=OPENAI_MODEL)
message = HumanMessagePromptTemplate.from_template(template=PROMPT_INFO)
chat_prompt = ChatPromptTemplate.from_messages([message])

query_q = input("Enter the query: ")


def get_info(query_q):
    # print("collecting data")

    chat_prompt_with_values = chat_prompt.format_prompt(
        query=query_q, format_instructions=parser.get_format_instructions()
    )

    output = llm(chat_prompt_with_values.to_messages())
    info = parser.parse(output.content)
    info_dict = {"query": info.query, "repnb": info.repnb, "projectid": info.projectid}
    repnb: list = info_dict["repnb"]
    projectid: list = info_dict["projectid"]

    specific = False
    if (len(repnb) > 0) | (len(projectid) > 0):
        specific = True
    if len(repnb) == 0:
        del info_dict["repnb"]
    if len(projectid) == 0:
        del info_dict["projectid"]

    return info_dict, specific
    # return info, ""
    # print(info)
    # print(len(repnb), len(projectid))
    # print(info_dict, specific)


print(get_info(query_q))
