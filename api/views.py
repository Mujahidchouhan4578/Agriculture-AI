import os
import tempfile

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from agents.pdf_agent import PDFAgent
from agents.parser_agent import ParserAgent
from django.shortcuts import render

import os
import tempfile

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from agents.pdf_agent import PDFAgent
from agents.parser_agent import ParserAgent
from agents.crop_agent import CropAgent
from agents.deficit_agent import DeficitAgent
from agents.recommendation_agent import RecommendationAgent
from agents.calculation_agent import CalculationAgent


@csrf_exempt
def analyze_farm(request):

    if request.method != "POST":

        return JsonResponse({
            "success": False,
            "error": "POST request required"
        }, status=405)


    # ==========================================
    # GET USER INPUT
    # ==========================================

    crop = request.POST.get("crop")

    area = request.POST.get("area")

    area_unit = request.POST.get("area_unit")

    soil_report = request.FILES.get("soil_report")


    # ==========================================
    # VALIDATION
    # ==========================================

    if not soil_report:

        return JsonResponse({
            "success": False,
            "error": "Soil report is required"
        }, status=400)


    if not crop:

        return JsonResponse({
            "success": False,
            "error": "Crop is required"
        }, status=400)


    if not area:

        return JsonResponse({
            "success": False,
            "error": "Area is required"
        }, status=400)


    if not area_unit:

        return JsonResponse({
            "success": False,
            "error": "Area unit is required"
        }, status=400)


    temp_path = None


    try:

        # ==========================================
        # SAVE PDF TEMPORARILY
        # ==========================================

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            for chunk in soil_report.chunks():

                temp_file.write(chunk)

            temp_path = temp_file.name


        # ==========================================
        # INITIAL STATE
        # ==========================================

        state = {

            "pdf_path": temp_path,

            "crop": crop,

            "area": float(area),

            "area_unit": area_unit,

            "pdf_text": "",

            "soil_data": {},

            "crop_requirements": {},

            "nutrient_deficit": {},

            "recommendation": {},

            "calculated_fertilizers": []

        }


        # ==========================================
        # STATE 1
        # PDF AGENT
        # ==========================================

        pdf_agent = PDFAgent()

        state = pdf_agent.execute(state)


        # ==========================================
        # STATE 2
        # PARSER AGENT
        # ==========================================

        parser_agent = ParserAgent()

        state = parser_agent.execute(state)


        # ==========================================
        # STATE 3
        # CROP AGENT
        # ==========================================

        crop_agent = CropAgent()

        state = crop_agent.execute(state)


        # ==========================================
        # STATE 4
        # DEFICIT AGENT
        # ==========================================

        deficit_agent = DeficitAgent()

        state = deficit_agent.execute(state)


        # ==========================================
        # STATE 5
        # RECOMMENDATION AGENT
        # ==========================================

        recommendation_agent = RecommendationAgent()

        state = recommendation_agent.execute(state)


        # ==========================================
        # STATE 6
        # CALCULATION AGENT
        # ==========================================

        calculation_agent = CalculationAgent()

        state = calculation_agent.execute(state)


        # ==========================================
        # RETURN EVERYTHING TO FRONTEND
        # ==========================================

        return JsonResponse({

            "success": True,

            "data": {

                "crop": state["crop"],

                "area": state["area"],

                "area_unit": state["area_unit"],

                "soil_data": state["soil_data"],

                "crop_requirements":
                    state["crop_requirements"],

                "nutrient_deficit":
                    state["nutrient_deficit"],

                "recommendation":
                    state["recommendation"]

            }

        })


    except Exception as e:

        print("================================")
        print("MAHSOUL ERROR")
        print(str(e))
        print("================================")


        return JsonResponse({

            "success": False,

            "error": str(e)

        }, status=500)


    finally:

        # ==========================================
        # DELETE TEMP PDF
        # ==========================================

        if temp_path and os.path.exists(temp_path):

            os.remove(temp_path)
def home(request):
    return render(request, "index.html")

