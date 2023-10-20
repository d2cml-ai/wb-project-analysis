import openai
import streamlit as st
from dotenv import load_dotenv

import os

load_dotenv()

def main():
	st.markdown('hola')

A = os.getenv('OPENAI_KEY')
print(A)

# openai.api_key = os.getenv('OPENAIKEY')

# if __name__ == '__main__':
# 	main()