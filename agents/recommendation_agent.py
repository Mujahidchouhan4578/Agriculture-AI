from llm.service import LLMServices
from prompt.recommendation_prompt import RECOMMENDATION_PROMPT
import json

class RecommendationAgent:

    def __init__(self):
        self.llm = LLMServices()

    def execute(self, state):
        crop = state["crop"]

        area = state["area"]

        area_unit = state["area_unit"]

        soil_data = state["soil_data"]
        
        nutrient_deficit=state["nutrient_deficit"]
        crop_requirements = state["crop_requirements"]
        prompt=RECOMMENDATION_PROMPT.format(
            crop=crop,
            area=area,
            area_unit=area_unit,
            soil_data=soil_data,
            crop_requirements=crop_requirements,
            nutrient_deficit=nutrient_deficit
        )    
        
        response=self.llm.ask(prompt)
       
      
        cleaned=(
            response.replace("```json","")
                    .replace("```","")
                    .strip()
                    
        )
        
       
        recommendation=json.loads(cleaned)    
        state["recommendation"]=recommendation
        return  state