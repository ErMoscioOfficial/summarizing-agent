from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.chains import LLMChain
from pydantic import BaseModel, Field
from typing import List

from routes.summarize.schema import ConversationSummary

parser = PydanticOutputParser(pydantic_object=ConversationSummary)

llm = Ollama(model="mistral")

prompt = PromptTemplate(
    template=(
        "You are an expert summarizer for workplace chat conversations.\n"
        "Given the following conversation between coworkers on a Teams channel, extract the key information.\n\n"
        "Avoid small talk and irrelevant details. Write the summary professionally and clearly."
        "I am {first_name} {last_name}, use this as a reference for my personal action items."
        "{format_instructions}\n\n"
        "Conversation:\n{text}\n"
    ),
    input_variables=["text", "first_name", "last_name"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

summarization_chain = LLMChain(llm=llm, prompt=prompt)