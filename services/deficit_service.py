class DeficitService:
    def calculate(self,soil_data,crop_requirements):
        deficit={}
        for nutrient,required in crop_requirements.items():
            available=soil_data.get(nutrient,0)
            if available is None:
                available=0
                
            deficit[nutrient]=max(0,required-available)
            
        return deficit
    