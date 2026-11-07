from services.deficit_service import DeficitService

class DeficitAgent:
    def __init__(self):
        self.service=DeficitService()
        
    def execute(self,state):
        state["nutrient_deficit"]=self.service.calculate(state["soil_data"],state["crop_requirements"])
        
        return state