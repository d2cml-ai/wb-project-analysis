# possible addition to the routher prompt
# You will assist in classifying whether a question is about a general topic or about a specific document.

# For this, you will output a number and, if the question is about a specific document, you will output the document ID.

# Each ID consists of a P followed by a 7 digit number, although users might not include the P and only refer to the number in their question

# Whenever the user asks about a document with a specific ID, you will output: "1, <<ID>>"

# When the user asks about a general topic, you will output "2, None"

# Here are a few examples of how this should function:

router_prompt = """
Question: What can you tell me about document 2055454?

Answer: P2055454

Question: What can you tell me about projects on healthcare infrastructure?

Answer: False

Question: Summarize document 8542857

Answer: P8542857

Question: 5G

Answer: False

Question: 4571

Answer: False

Question: 4358971

Answer: P4358971
"""

project_question_system_prompt = """
Answer the user's query specifically using the user-provided information.
"""

project_question_user_prompt = """
Query: {query}

Information:
{context}
"""