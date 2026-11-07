from llm.service import LLMServices
from prompt.parser_prompt import  PARSER_PROMPT
import json
class ParserAgent:
    def __init__(self):
        self.llm=LLMServices()
            
    def execute(self,state):
        pdf_text=state["pdf_text"]
        prompt=PARSER_PROMPT.format(soil_report=pdf_text)
        response=self.llm.ask(prompt)

        # Remove markdown code fences
        cleaned_response = (
            response.replace("```json", "")
                    .replace("```", "")
                    .strip()
        )

   # Convert JSON string to Python dictionary
        soil_data = json.loads(cleaned_response)
        state["soil_data"]=soil_data
        return state