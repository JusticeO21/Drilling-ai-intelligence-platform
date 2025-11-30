def format_metadata_for_llm(metadata: dict) -> str:
    """Format comprehensive metadata into readable text for LLM"""
    lines = []

    # Dataset-level information
    if metadata.get("dataset"):
        ds = metadata["dataset"]
        lines.append(f"DATASET OVERVIEW:")
        lines.append(f"Name: {ds.get('dataset_name', 'Unknown')}")
        lines.append(f"Total Rows: {ds.get('num_rows', 0):,}")
        lines.append(f"Total Columns: {ds.get('num_cols', 0)}")
        lines.append(f"Memory Usage: {ds.get('memory_usage_mb', 0):.2f} MB")
        lines.append(
            f"Description: {ds.get('description', 'No description available')}"
        )
        lines.append("")

        # Data quality metrics
        lines.append("DATA QUALITY METRICS:")
        lines.append(f"Total Null Cells: {ds.get('total_null_cells', 0):,}")
        lines.append(
            f"Overall Null Percentage: {ds.get('overall_null_percentage', 0):.2f}%"
        )
        lines.append(f"Complete Rows: {ds.get('complete_rows', 0):,}")
        lines.append(
            f"Complete Rows Percentage: {ds.get('complete_rows_percentage', 0):.2f}%"
        )
        lines.append(f"Duplicate Rows: {ds.get('duplicate_rows', 0):,}")
        lines.append(
            f"Duplicate Rows Percentage: {ds.get('duplicate_rows_percentage', 0):.2f}%"
        )
        lines.append("")

        # Column type distribution
        if ds.get("column_types"):
            lines.append("COLUMN TYPE DISTRIBUTION:")
            for dtype, count in ds["column_types"].items():
                lines.append(f"  {dtype}: {count} columns")
            lines.append("")

        # Special column categories
        categories = [
            ("Numeric Columns", ds.get("numeric_columns", [])),
            ("Categorical Columns", ds.get("categorical_columns", [])),
            ("DateTime Columns", ds.get("datetime_columns", [])),
            ("Percentage Columns", ds.get("percentage_columns", [])),
            ("ID Columns", ds.get("id_columns", [])),
        ]

        for category_name, columns in categories:
            if columns:
                lines.append(f"{category_name.upper()}:")
                lines.append(f"  {', '.join(columns)}")
                lines.append("")

    # Column-level information
    if metadata.get("columns"):
        lines.append("COLUMN DETAILS:")
        lines.append("=" * 50)

        for col in metadata["columns"]:
            lines.append(f"\nCOLUMN: {col['column']}")
            lines.append(f"Type: {col['type']}")
            lines.append(f"Description: {col.get('description', 'No description')}")
            lines.append(f"Relevance Score: {col.get('relevance_score', 0):.4f}")
            lines.append("")

            stats = col.get("stats", {})

            # Basic stats (all columns)
            if any(key in stats for key in ["count", "total_rows", "null_count"]):
                lines.append("  BASIC STATISTICS:")
                lines.append(f"    Count: {stats.get('count', 'N/A')}")
                lines.append(f"    Total Rows: {stats.get('total_rows', 'N/A')}")
                lines.append(f"    Null Count: {stats.get('null_count', 'N/A')}")
                lines.append(
                    f"    Null Percentage: {stats.get('null_percentage', 'N/A')}"
                )
                lines.append(f"    Unique Values: {stats.get('unique_count', 'N/A')}")
                lines.append("")

            # Numerical statistics
            numerical_stats = [
                "mean",
                "median",
                "std",
                "variance",
                "min",
                "max",
                "range",
                "q25",
                "q75",
                "skewness",
                "kurtosis",
            ]
            if any(stats.get(stat) is not None for stat in numerical_stats):
                lines.append("  NUMERICAL STATISTICS:")
                for stat in numerical_stats:
                    value = stats.get(stat)
                    if value is not None:
                        if isinstance(value, float):
                            lines.append(f"    {stat.title()}: {value:.4f}")
                        else:
                            lines.append(f"    {stat.title()}: {value}")
                lines.append("")

            # Categorical statistics
            categorical_stats = ["top_value", "top_value_freq", "top_value_percentage"]
            if any(stats.get(stat) is not None for stat in categorical_stats):
                lines.append("  CATEGORICAL STATISTICS:")
                for stat in categorical_stats:
                    value = stats.get(stat)
                    if value is not None:
                        lines.append(f"    {stat.replace('_', ' ').title()}: {value}")
                lines.append("")

                # Top 5 values if available
                if stats.get("top_5_values"):
                    lines.append("    Top 5 Values:")
                    for item in stats["top_5_values"][:5]:
                        lines.append(f"      {item['value']}: {item['count']} times")

            # Boolean statistics
            boolean_stats = ["true_count", "false_count", "true_percentage"]
            if any(stats.get(stat) is not None for stat in boolean_stats):
                lines.append("  BOOLEAN STATISTICS:")
                for stat in boolean_stats:
                    value = stats.get(stat)
                    if value is not None:
                        lines.append(f"    {stat.replace('_', ' ').title()}: {value}")
                lines.append("")

            # Datetime statistics
            datetime_stats = ["min_date", "max_date", "date_range_days"]
            if any(stats.get(stat) is not None for stat in datetime_stats):
                lines.append("  DATETIME STATISTICS:")
                for stat in datetime_stats:
                    value = stats.get(stat)
                    if value is not None:
                        lines.append(f"    {stat.replace('_', ' ').title()}: {value}")
                lines.append("")

            lines.append("-" * 30)

    return "\n".join(lines)
