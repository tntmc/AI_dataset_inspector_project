from reasoning.reason_schema import ReasoningContext

# def build_reasoning_context(dataset_profile, missing_by_column, duplicate_rows_count):
def build_reasoning_context(dataset_profile: dict) -> ReasoningContext:
    meta = dataset_profile["Metadata"]
    missing_by_column = dataset_profile["missing_values"]["missing_by_column"]
    duplicate_rows = dataset_profile["duplicate_rows_count"]["duplicate_count"]

    return ReasoningContext(
      dataset_overview={
        "rows": meta['n_for_rows'],
        "columns": meta['n_for_columns'],
        "columns_names": meta.get("columns", [])
      },
      missing_summary=missing_by_column,
      duplicate_rows=duplicate_rows
    )
