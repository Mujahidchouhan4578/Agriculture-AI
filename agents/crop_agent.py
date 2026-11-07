import json
from llm.service import LLMServices
from prompt.crop_prompt import CROP_PROMPT

class CropAgent:
    def __init__(self):
        self.llm=LLMServices()
        
        
    def execute(self,state):
        
        crop=state["crop"]
        print(f"we are doing for crop {crop} ")
        prompt=CROP_PROMPT.format(crop=crop)
        response=self.llm.ask(prompt)
        cleaned_response=(
            response.replace("```json","")
                    .replace("```","")
                    .strip()
            
        )
        
        crop_requirements=json.loads(cleaned_response)
        state["crop_requirements"]=crop_requirements
        return state