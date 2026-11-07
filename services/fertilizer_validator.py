class FertilizerValidator:

    VALID_NUTRIENTS = {
        "nitrogen",
        "phosphorus",
        "potassium",
        "sulphur"
    }

    VALID_BASES = {
        "N",
        "P",
        "P2O5",
        "K",
        "K2O",
        "S"
    }

    def validate(self, recommendation):

        fertilizers = recommendation.get(
            "recommended_fertilizers",
            []
        )

        validated = []

        for fertilizer in fertilizers:

            name = fertilizer.get("name")
            grade = fertilizer.get("grade")
            target_nutrient = fertilizer.get("target_nutrient")
            nutrient_basis = fertilizer.get("nutrient_basis")
            composition = fertilizer.get(
                "composition_percent"
            )

            # -------------------------
            # Required fields
            # -------------------------

            if not name:
                raise ValueError(
                    "Fertilizer name is missing"
                )

            if not grade:
                raise ValueError(
                    f"Grade missing for {name}"
                )

            if not target_nutrient:
                raise ValueError(
                    f"Target nutrient missing for {name}"
                )

            if not nutrient_basis:
                raise ValueError(
                    f"Nutrient basis missing for {name}"
                )

            # -------------------------
            # Nutrient validation
            # -------------------------

            if target_nutrient.lower() not in self.VALID_NUTRIENTS:

                raise ValueError(
                    f"Invalid nutrient: {target_nutrient}"
                )

            # -------------------------
            # Basis validation
            # -------------------------

            if nutrient_basis not in self.VALID_BASES:

                raise ValueError(
                    f"Invalid nutrient basis: {nutrient_basis}"
                )

            # -------------------------
            # Composition validation
            # -------------------------

            if not isinstance(
                composition,
                (int, float)
            ):

                raise ValueError(
                    f"Invalid composition for {name}"
                )

            if composition <= 0 or composition > 100:

                raise ValueError(
                    f"Invalid composition percentage "
                    f"for {name}: {composition}"
                )

            # -------------------------
            # Store validated fertilizer
            # -------------------------

            validated.append({
                "name": name,
                "grade": grade,
                "target_nutrient": target_nutrient,
                "nutrient_basis": nutrient_basis,
                "composition_percent": composition,
                "reason": fertilizer.get(
                    "reason",
                    ""
                )
            })

        return validated