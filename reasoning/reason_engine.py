from reasoning.reason_schema import ReasoningResults

def run_reasoning(context):
    insights = []
    recommendations = []
    risk = "LOW"
    for col, ratio in context.missing_summary.items():
        if ratio > 0.3:
            risk = "HIGH"
            insights.append(
                f"Column '{col}' has a high missing ratio ({ratio:.0%})."
            )
            recommendations.append(
                f"Consider imputing or dropping column '{col}'."
            )

        elif ratio <= 0.3 and ratio > 0.1:
            if risk != "HIGH":
                risk = "MEDIUM"

            insights.append(
                f"Column '{col}' has moderate missing values ({ratio:.0%})."
            )
            recommendations.append(
                f"Consider imputing column '{col}'."
            )

        elif ratio <= 0.1 and ratio > 0:
            insights.append(
                f"Column '{col}' has low missing values ({ratio:.0%})."
            )

    if context.duplicate_rows > 0:
        insights.append(
            f"Dataset contains {context.duplicate_rows} duplicate rows."
        )
        recommendations.append("Remove duplicate rows.")

        if risk != "HIGH":
            risk = "MEDIUM"

    if not insights:
        insights.append("Dataset quality looks good overall.")

    return ReasoningResults(
        risk_levels=risk,
        insights=insights,
        recommendations=recommendations
    )
