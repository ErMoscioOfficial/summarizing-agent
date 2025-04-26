from routes.summarize.schema import ConversationSummary

from routes.summarize.chain import summarization_chain, parser

class SummarizationService:
    async def summarize_text(self, text: str, first_name : str, last_name : str) -> ConversationSummary:
        model_output = await summarization_chain.arun(
            text=text, 
            first_name = first_name, 
            last_name = last_name
        )
        
        parsed_output = parser.parse(model_output)
        return parsed_output

