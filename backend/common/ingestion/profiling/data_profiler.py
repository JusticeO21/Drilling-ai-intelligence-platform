from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
from datetime import datetime


class DataFrameProfiler:
    """
    Comprehensive DataFrame profiler for extracting column and dataset-level statistics.
    Optimized for well log data and general tabular datasets.
    """

    def __init__(self, df: pd.DataFrame, dataset_name: str = None):
        """
        Initialize profiler with a DataFrame.

        Args:
            df: Pandas DataFrame to profile
            dataset_name: Optional name for the dataset
        """
        self.df = df
        self.dataset_name = dataset_name or "Unnamed Dataset"
        self.num_rows = len(df)
        self.num_cols = len(df.columns)

    def profile_column(self, col: str) -> Dict[str, Any]:
        """
        Generate comprehensive statistics for a single column.

        Args:
            col: Column name

        Returns:
            Dictionary containing all relevant statistics
        """
        series = self.df[col]
        col_type = str(series.dtype)

        # Base stats for all columns
        stats = {
            "column": col,
            "type": col_type,
            "count": int(series.count()),
            "total_rows": self.num_rows,
            "null_count": int(series.isna().sum()),
            "null_percentage": float((series.isna().sum() / self.num_rows) * 100),
        }

        # Numerical columns
        if pd.api.types.is_numeric_dtype(series):
            non_null = series.dropna()

            if len(non_null) > 0:
                stats.update(
                    {
                        "mean": float(non_null.mean()),
                        "median": float(non_null.median()),
                        "std": float(non_null.std()),
                        "min": float(non_null.min()),
                        "max": float(non_null.max()),
                        "q25": float(non_null.quantile(0.25)),
                        "q75": float(non_null.quantile(0.75)),
                        "variance": float(non_null.var()),
                        "range": float(non_null.max() - non_null.min()),
                    }
                )

                stats["skewness"] = float(non_null.skew())
                stats["kurtosis"] = float(non_null.kurtosis())
                stats["unique_count"] = int(series.nunique())

                if stats["unique_count"] < 20:
                    value_counts = series.value_counts()
                    stats["top_value"] = str(value_counts.index[0])
                    stats["top_value_freq"] = int(value_counts.iloc[0])

        elif pd.api.types.is_object_dtype(series) or pd.api.types.is_categorical_dtype(
            series
        ):
            non_null = series.dropna()

            stats["unique_count"] = int(series.nunique())

            if len(non_null) > 0:
                value_counts = series.value_counts()
                stats["top_value"] = str(value_counts.index[0])
                stats["top_value_freq"] = int(value_counts.iloc[0])
                stats["top_value_percentage"] = float(
                    (value_counts.iloc[0] / len(non_null)) * 100
                )

                top_5 = value_counts.head(5)
                stats["top_5_values"] = [
                    {"value": str(val), "count": int(count)}
                    for val, count in top_5.items()
                ]

        # Datetime columns
        elif pd.api.types.is_datetime64_any_dtype(series):
            non_null = series.dropna()

            if len(non_null) > 0:
                stats.update(
                    {
                        "min_date": str(non_null.min()),
                        "max_date": str(non_null.max()),
                        "date_range_days": int((non_null.max() - non_null.min()).days),
                    }
                )

        # Boolean columns
        elif pd.api.types.is_bool_dtype(series):
            value_counts = series.value_counts()
            stats["true_count"] = int(value_counts.get(True, 0))
            stats["false_count"] = int(value_counts.get(False, 0))
            stats["true_percentage"] = float(
                (value_counts.get(True, 0) / self.num_rows) * 100
            )

        return stats

    def profile_all_columns(self) -> List[Dict[str, Any]]:
        """
        Profile all columns in the DataFrame.

        Returns:
            List of dictionaries containing stats for each column
        """
        return [self.profile_column(col) for col in self.df.columns]

    def get_dataset_stats(self) -> Dict[str, Any]:
        """
        Generate dataset-level statistics and metadata.

        Returns:
            Dictionary containing dataset-level information
        """
        stats = {
            "dataset_name": self.dataset_name,
            "num_rows": self.num_rows,
            "num_cols": self.num_cols,
            "columns": list(self.df.columns),
            "memory_usage_mb": float(
                self.df.memory_usage(deep=True).sum() / (1024 * 1024)
            ),
            "indexed_at": datetime.utcnow().isoformat(),
        }

        # Column type distribution
        type_counts = self.df.dtypes.value_counts()
        stats["column_types"] = {
            str(dtype): int(count) for dtype, count in type_counts.items()
        }

        # Overall data quality
        total_cells = self.num_rows * self.num_cols
        total_nulls = self.df.isna().sum().sum()
        stats["total_null_cells"] = int(total_nulls)
        stats["overall_null_percentage"] = float((total_nulls / total_cells) * 100)
        stats["complete_rows"] = int(self.df.dropna().shape[0])
        stats["complete_rows_percentage"] = float(
            (stats["complete_rows"] / self.num_rows) * 100
        )

        # Identify column categories by name patterns
        stats["percentage_columns"] = [
            col for col in self.df.columns if "%" in col or "percent" in col.lower()
        ]
        stats["id_columns"] = [
            col
            for col in self.df.columns
            if "id" in col.lower() or col.lower().endswith("_id")
        ]
        stats["numeric_columns"] = list(
            self.df.select_dtypes(include=[np.number]).columns
        )
        stats["categorical_columns"] = list(
            self.df.select_dtypes(include=["object", "category"]).columns
        )
        stats["datetime_columns"] = list(
            self.df.select_dtypes(include=["datetime64"]).columns
        )

        # Duplicate rows
        stats["duplicate_rows"] = int(self.df.duplicated().sum())
        stats["duplicate_rows_percentage"] = float(
            (stats["duplicate_rows"] / self.num_rows) * 100
        )

        return stats

    def get_correlation_matrix(
        self, method: str = "pearson"
    ) -> Optional[Dict[str, Dict[str, float]]]:
        """
        Calculate correlation matrix for numerical columns.

        Args:
            method: Correlation method ('pearson', 'spearman', 'kendall')

        Returns:
            Dictionary representation of correlation matrix
        """
        numeric_df = self.df.select_dtypes(include=[np.number])

        if numeric_df.shape[1] < 2:
            return None

        corr_matrix = numeric_df.corr(method=method)

        # Convert to nested dict for easy JSON serialization
        return {
            col: {
                other_col: float(corr_matrix.loc[col, other_col])
                for other_col in corr_matrix.columns
            }
            for col in corr_matrix.index
        }

    def get_top_correlations(
        self, threshold: float = 0.5, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get top correlated column pairs (excluding self-correlation).

        Args:
            threshold: Minimum absolute correlation to include
            limit: Maximum number of pairs to return

        Returns:
            List of correlation pairs sorted by absolute correlation
        """
        corr_matrix = self.get_correlation_matrix()

        if not corr_matrix:
            return []

        correlations = []
        seen_pairs = set()

        for col1 in corr_matrix:
            for col2 in corr_matrix[col1]:
                if col1 == col2:
                    continue

                # Avoid duplicate pairs (A-B and B-A)
                pair = tuple(sorted([col1, col2]))
                if pair in seen_pairs:
                    continue

                seen_pairs.add(pair)
                corr_value = corr_matrix[col1][col2]

                if abs(corr_value) >= threshold:
                    correlations.append(
                        {
                            "column_1": col1,
                            "column_2": col2,
                            "correlation": float(corr_value),
                            "abs_correlation": float(abs(corr_value)),
                        }
                    )

        # Sort by absolute correlation descending
        correlations.sort(key=lambda x: x["abs_correlation"], reverse=True)

        return correlations[:limit]

    def create_column_description(self, col: str, stats: Dict[str, Any]) -> str:
        """
        Create semantic description for a column (for embedding).

        Args:
            col: Column name
            stats: Statistics dictionary from profile_column()

        Returns:
            Rich semantic description string
        """
        parts = [f"{col} is a {stats['type']} column"]

        # Numerical columns
        if stats.get("mean") is not None:
            parts.append("representing numerical measurements")
            parts.append(f"ranging from {stats['min']:.2f} to {stats['max']:.2f}")
            parts.append(f"with an average of {stats['mean']:.2f}")

            # Domain-specific hints
            if "temp" in col.lower() or "temperature" in col.lower():
                parts.append("measuring temperature")
            elif "depth" in col.lower():
                parts.append("indicating depth of a well or vertical position")
            elif "%" in col or "percent" in col.lower():
                parts.append("expressed as a percentage or proportion")
            elif any(x in col.upper() for x in ["DT", "SONIC"]):
                parts.append("from sonic log measurements in microseconds per foot")
            elif any(x in col.upper() for x in ["GR", "GAMMA"]):
                parts.append("from gamma ray log readings in API units")
            elif "pressure" in col.lower():
                parts.append("measuring pressure")
            elif "porosity" in col.lower():
                parts.append("representing rock porosity")

        # Categorical columns
        elif stats.get("unique_count"):
            parts.append("containing categorical data")
            parts.append(f"with {stats['unique_count']} unique values")
            if stats.get("top_value"):
                parts.append(
                    f"most frequently '{stats['top_value']}' ({stats.get('top_value_percentage', 0):.1f}%)"
                )

        # Datetime columns
        elif stats.get("min_date"):
            parts.append("containing datetime values")
            parts.append(f"spanning from {stats['min_date']} to {stats['max_date']}")

        # Data quality
        if stats["null_percentage"] > 0:
            parts.append(f"with {stats['null_percentage']:.1f}% missing values")
        elif stats["null_percentage"] == 0:
            parts.append("with no missing values")

        return ". ".join(parts) + "."

    def create_dataset_description(self, dataset_stats: Dict[str, Any]) -> str:
        """
        Create semantic description for the entire dataset (for embedding).

        Args:
            dataset_stats: Statistics from get_dataset_stats()

        Returns:
            Rich semantic description string
        """
        parts = [f"Dataset named {dataset_stats['dataset_name']}"]
        parts.append(
            f"containing {dataset_stats['num_rows']} rows and {dataset_stats['num_cols']} columns"
        )

        # Column categorization
        if dataset_stats.get("percentage_columns"):
            parts.append(
                f"includes percentage measurements: {', '.join(dataset_stats['percentage_columns'][:5])}"
            )

        if dataset_stats.get("numeric_columns"):
            parts.append(
                f"has {len(dataset_stats['numeric_columns'])} numerical columns"
            )

        if dataset_stats.get("categorical_columns"):
            parts.append(
                f"has {len(dataset_stats['categorical_columns'])} categorical columns"
            )

        # Data quality
        if dataset_stats["overall_null_percentage"] > 0:
            parts.append(
                f"with {dataset_stats['overall_null_percentage']:.1f}% missing data overall"
            )
        else:
            parts.append("with complete data and no missing values")

        # List all columns
        parts.append(f"Columns include: {', '.join(dataset_stats['columns'])}")

        return ". ".join(parts) + "."

    def generate_full_profile(self) -> Dict[str, Any]:
        """
        Generate complete profile with all statistics.

        Returns:
            Comprehensive dictionary with dataset and column stats
        """
        dataset_stats = self.get_dataset_stats()
        column_stats = self.profile_all_columns()
        correlations = self.get_top_correlations()

        # Add descriptions for embedding
        dataset_stats["description"] = self.create_dataset_description(dataset_stats)

        for col_stat in column_stats:
            col_stat["description"] = self.create_column_description(
                col_stat["column"], col_stat
            )

        return {
            "dataset": dataset_stats,
            "columns": column_stats,
            "correlations": correlations,
            "profile_generated_at": datetime.utcnow().isoformat(),
        }
