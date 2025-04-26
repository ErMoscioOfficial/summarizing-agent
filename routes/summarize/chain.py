from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.chains import LLMChain
from pydantic import BaseModel, Field
from typing import List

from routes.summarize.schema import ConversationSummary

#parser = PydanticOutputParser(pydantic_object=ConversationSummary)

llm = Ollama(model="tinyllama")

prompt = PromptTemplate(
    template=(
        "You are a helpful assistant."
        "Summarize the following conversation in a clear and concise way. Focus on the key points and main decisions made."
        "I am {first_name} {last_name}"
        "Conversation:"
        "{text}"
        "Summary:"
    ),
    input_variables=["text", "first_name", "last_name"]
    #partial_variables={"format_instructions": parser.get_format_instructions()}
)

summarization_chain = LLMChain(llm=llm, prompt=prompt)