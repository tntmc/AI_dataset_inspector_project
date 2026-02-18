import pandas as pd
import numpy as np


def generate_dataset_profile(df: pd.DataFrame) -> dict:
  profile = {}

  # metadata
  memory_usage = round(df.memory_usage(deep=True).sum() / (1024 ** 2), 3)

  profile['Metadata'] = {
    "n_for_rows" : df.shape[0],
    "n_for_columns" : df.shape[1],
    "columns" : df.columns.tolist(),
    "memory_usage" : f"{memory_usage} MB" # in MB
  }


  # data types
  data_types = {
    "numeric": [],
    "categorical": [],
    "datetime": [],
    "text": [],
    "boolean": [],
    "other": []
  }

  for col in df.columns:
    if pd.api.types.is_numeric_dtype(df[col]):
      data_types["numeric"].append(col)
    elif pd.api.types.is_categorical_dtype(df[col]) or pd.api.types.is_object_dtype(df[col]):
      data_types["categorical"].append(col)
    elif pd.api.types.is_datetime64_any_dtype(df[col]):
      data_types["datetime"].append(col)
    elif pd.api.types.is_bool_dtype(df[col]):
      data_types["boolean"].append(col)
    elif pd.api.types.is_string_dtype(df[col]):
      data_types["text"].append(col)
    else:
      data_types["other"].append(col)


  profile['Data Types'] = data_types


  # missing values
  missing_values = df.isna().mean()

  profile['missing_values'] = {
    "total_missing_percentage": round(missing_values.mean() * 100, 2),
    "missing_by_column": missing_values.round(3).to_dict(),
    "risk_levels": {
      "high_risk": missing_values[missing_values > 0.3].index.tolist(),
      "medium_risk" : missing_values[(missing_values > 0.1) & (missing_values <= 0.3)].index.tolist(),
      "low_risk" : missing_values[(missing_values > 0) & (missing_values <= 0.1)].index.tolist()
    }
  }

  # duplicate rows
  duplicate_count = df.duplicated().sum()
  profile['duplicate_rows_count'] = {
    "duplicate_count": int(duplicate_count),
    "duplicate_percentage": round((duplicate_count / len(df)) * 100, 2) if len(df) > 0 else 0.0
  }

  #  basic statistics
  stats = {}

  for col in data_types["numeric"]:
    stats[col] = {
      "min": round(df[col].min(), 3),
      "max": round(df[col].max(), 3),
      "mean": round(df[col].mean(), 3),
      "median": round(df[col].median(), 3),
      "std": round(df[col].std(), 3)
    }

  profile['basic_statistics'] = {
    "numerical_summary": stats,
  }

  #  anomalities values / potetial outlier atau issues
  anomalities = {
    "high_cardinality_columns": [],
    "constant_columns": [],
    "date_columns_with_future_dates": [],
    "id_like_columns": []
  }


  for col in df.columns:
    unique_ratio = df[col].nunique() / len(df) if len(df) > 0 else 0

    #  high cardinality check
    if unique_ratio > 0.9:
      anomalities["high_cardinality_columns"].append(col)

    #  constant columns
    if df[col].nunique() == 1:
      anomalities["constant_columns"].append(col)

    # date columns with future dates
    if pd.api.types.is_datetime64_any_dtype(df[col]):
      if (df[col] > pd.Timestamp.now()).any():
        anomalities["date_columns_with_future_dates"].append(col)

    # id-like columns
    try:
      if col.lower().endswith(("id", "_id")):
        anomalities["id_like_columns"].append(col)
    except AttributeError:
      pass

  profile['anomalities'] = anomalities

  return profile