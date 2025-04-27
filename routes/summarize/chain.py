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
        "You are a helpful assistant.\n"
        "Focus only on the new information or decisions in the conversation.\n"
        "Provide a summary of only what's new based on the previous summary and the new messages.\n"
        "Ignore any old context that is not directly relevant to what's new.\n"
        "Previous Summary:\n{previous_summary}\n\n"
        "New Messages:\n{new_messages}\n\n"
        "Only the new summary of what's changed or been added:"
    ),
    input_variables=["previous_summary", 'new_messages']
    #partial_variables={"format_instructions": parser.get_format_instructions()}
)

summarization_chain = LLMChain(llm=llm, prompt=prompt)