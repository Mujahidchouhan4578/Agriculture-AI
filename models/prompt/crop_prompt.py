CROP_PROMPT = """
You are an agricultural expert.

For the given crop, estimate the recommended nutrient requirement
per acre.

Return ONLY valid JSON.

Fields:

nitrogen
phosphorus
potassium
sulphur

Crop:

{crop}
"""