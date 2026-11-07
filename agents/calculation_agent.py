class CalculationAgent:

    def execute(self, state):

        recommendation = state["recommendation"]
        deficits = state["nutrient_deficit"]

        # Make sure recommendation exists
        if not recommendation:
            raise ValueError(
                "No fertilizer recommendation found."
            )

        fertilizers = recommendation.get(
            "recommended_fertilizers", []
        )

        if not fertilizers:
            raise ValueError(
                "No fertilizers were recommended by LLM."
            )

        for fertilizer in fertilizers:

            # =====================================================
            # 1. Validate required fields
            # =====================================================

            required_fields = [
                "target_nutrient",
                "composition_percent",
                "density_kg_per_litre",
                "conversion_required"
            ]

            for field in required_fields:

                if field not in fertilizer:

                    raise ValueError(
                        f"LLM did not provide required field: "
                        f"{field}"
                    )

            # =====================================================
            # 2. Normalize nutrient name
            # =====================================================

            nutrient = str(
                fertilizer["target_nutrient"]
            ).lower().strip()

            if "nitrogen" in nutrient:
                nutrient = "nitrogen"

            elif "phosphorus" in nutrient:
                nutrient = "phosphorus"

            elif "potassium" in nutrient:
                nutrient = "potassium"

            elif (
                "sulphur" in nutrient
                or "sulfur" in nutrient
            ):
                nutrient = "sulphur"

            else:

                raise ValueError(
                    f"Unknown nutrient: "
                    f"{fertilizer['target_nutrient']}"
                )

            # =====================================================
            # 3. Get nutrient deficiency
            # =====================================================

            deficit = deficits.get(nutrient)

            if deficit is None:

                raise ValueError(
                    f"No deficiency found for {nutrient}"
                )

            if deficit <= 0:

                raise ValueError(
                    f"Fertilizer recommended for {nutrient}, "
                    f"but deficiency is {deficit}."
                )

            # =====================================================
            # 4. Basis conversion
            # =====================================================

            conversion_required = fertilizer[
                "conversion_required"
            ]

            if conversion_required:

                conversion = fertilizer.get(
                    "conversion"
                )

                if not conversion:

                    raise ValueError(
                        "Conversion required but "
                        "conversion information is missing."
                    )

                factor = conversion.get(
                    "factor"
                )

                if factor is None:

                    raise ValueError(
                        "Conversion factor is missing."
                    )

                if not isinstance(
                    factor,
                    (int, float)
                ):

                    raise ValueError(
                        f"Invalid conversion factor: "
                        f"{factor}"
                    )

                if factor <= 0:

                    raise ValueError(
                        f"Invalid conversion factor: "
                        f"{factor}"
                    )

                converted_deficit = (
                    deficit * factor
                )

            else:

                converted_deficit = deficit

            # =====================================================
            # 5. Validate fertilizer composition
            # =====================================================

            composition_percent = fertilizer.get(
                "composition_percent"
            )

            if composition_percent is None:

                raise ValueError(
                    f"Composition is missing for fertilizer: "
                    f"{fertilizer.get('name')}"
                )

            if not isinstance(
                composition_percent,
                (int, float)
            ):

                raise ValueError(
                    f"Invalid composition for "
                    f"{fertilizer.get('name')}: "
                    f"{composition_percent}"
                )

            if (
                composition_percent <= 0
                or composition_percent > 100
            ):

                raise ValueError(
                    f"Invalid composition for "
                    f"{fertilizer.get('name')}: "
                    f"{composition_percent}%"
                )

            # Convert percentage to decimal

            composition = (
                composition_percent / 100
            )

            # =====================================================
            # 6. Validate density
            # =====================================================

            density = fertilizer.get(
                "density_kg_per_litre"
            )

            if density is None:

                raise ValueError(
                    f"Density is missing for fertilizer: "
                    f"{fertilizer.get('name')}"
                )

            if not isinstance(
                density,
                (int, float)
            ):

                raise ValueError(
                    f"Invalid density for "
                    f"{fertilizer.get('name')}: "
                    f"{density}"
                )

            if density <= 0:

                raise ValueError(
                    f"Invalid density for "
                    f"{fertilizer.get('name')}: "
                    f"{density}"
                )

            # =====================================================
            # 7. Calculate fertilizer quantity in kg
            # =====================================================

            fertilizer_kg = (
                converted_deficit /
                composition
            )

            # =====================================================
            # 8. Convert kg → litres
            # =====================================================

            quantity_litre = (
                fertilizer_kg /
                density
            )

            # =====================================================
            # 9. Store calculated values
            # =====================================================

            fertilizer["converted_deficit"] = round(
                converted_deficit,
                2
            )

            fertilizer["fertilizer_kg"] = round(
                fertilizer_kg,
                2
            )

            fertilizer["quantity_litre"] = round(
                quantity_litre,
                2
            )

        # =========================================================
        # Return updated state
        # =========================================================

        return state