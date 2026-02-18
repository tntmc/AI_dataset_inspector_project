# def apply_missing_value_rules(context):
#     insights = []

#     for col, ratio in context.quality_signals.missing_values.items():
#       if ratio > 0.3:
#           insights.append(
#               f"Column '{col}' has high missing ratio ({ratio:.0%}). Consider dropping or advanced imputation."
#           )
#       elif ratio > 0.1:
#           insights.append(
#               f"Column '{col}' has moderate missing values ({ratio:.0%}). Simple imputation may be sufficient."
#           )

#     return insights

# def apply_duplicate_rules(context):
#     if context.quality_signals.duplicate_rows > 0:
#         return [
#             f"Dataset contains {context.quality_signals.duplicate_rows} duplicate rows. Consider removing duplicates."
#         ]
#     return []