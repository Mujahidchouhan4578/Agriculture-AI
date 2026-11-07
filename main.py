from llm.client import ask_llm
from llm.service import LLMServices
from agents.pdf_agent import PDFAgent
from agents.parser_agent import ParserAgent
from agents.crop_agent import CropAgent
from agents.recommendation_agent import RecommendationAgent
from agents.deficit_agent import DeficitAgent
from services.fertilizer_validator import FertilizerValidator
from agents.calculation_agent import CalculationAgent
def main():

    state = {

        "pdf_path":"reports/sample.pdf",
        "crop":"rice",
        "area":4,
        "area_unit":"acre",
        "pdf_text":"",
        
        
        "soil_data":{},
        "crop_requirements":{},
        "nutrient_deficit":{},
        "recommendation":{},
        "validated_fertilizers":{},
        "calculated_fertilizers":[],
        

    }

    pdf = PDFAgent()

    state = pdf.execute(state)
    parser=ParserAgent()
    state=parser.execute(state)
    
    crop=CropAgent()
    state=crop.execute(state)
    
    deficit_service=DeficitAgent()
    state=deficit_service.execute(state)
    
    
    recommendation=RecommendationAgent()
    state=recommendation.execute(state)
    
    calculation=CalculationAgent()
    state=calculation.execute(state)
    

    print("\n===== SOIL DATA =====")
    print(state["soil_data"])

    print("\n===== CROP REQUIREMENTS =====")
    print(state["crop_requirements"])
    
    print("\n===== Deficiency =====")
    print(state["nutrient_deficit"])


    
    
    print("\n===== final  RECOMMENDATION =====")
    print(state["recommendation"])
    
    


if __name__=="__main__":
    main()
    
