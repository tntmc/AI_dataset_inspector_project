dataset_profile = {
    "basic_info": {
        "n_for_rows": int,
        "n_for_columns": int,
        "columns": list[str],
        "memory_usage": float
    },

    "Data_types": {
        "column_name": {
            "data_type": str,
            "inferred_type": "numeric | categorical | datetime | text"
        }
    },

    "missing_values": {
        "column_name": {
            "missing_count": int,
            "missing_percentage": float
        }
    },

    "duplicates": {
        "duplicate_rows_count": int,
        "duplicate_rows_percentage": float
    },

    "numerical_summary": {
        "column_name": {
            "min": float,
            "max": float,
            "mean": float,
            "median": float,
            "std": float
        }
    },

    "categorical_summary": {
        "column_name": {
            "unique_values": int,
            "unique_values_percentage": float,
            "top_values": dict  # value -> frequency
        }
    }
}
