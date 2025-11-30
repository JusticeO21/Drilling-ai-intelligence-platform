import re


def determine_metadata_needs(query: str) -> dict:
    """
    Decide what metadata to extract based on query type.

    Returns:
        {
            'need_columns': bool,
            'need_dataset': bool,
            'top_k': int
        }
    """
    query_lower = query.lower()

    # Pattern 1: Dataset-level queries ONLY
    dataset_only_patterns = [
        r"what datasets? do i have",
        r"list (all )?(my )?datasets",
        r"show (me )?(my )?datasets",
        r"how many datasets",
        r"which dataset(s)? (has|have|contains?)",
        r"overview of (my )?data",
    ]

    for pattern in dataset_only_patterns:
        if re.search(pattern, query_lower):
            return {"need_columns": True, "need_dataset": True, "top_k": 10}

    # Column-specific queries ONLY
    column_only_patterns = [
        r"(mean|average|median|std|min|max|range) of \w+",
        r"what('s| is) (the )?\w+ (column|field)",
        r"describe \w+ column",
        r"(statistics|stats) (for|of) \w+",
        r"null (count|percentage|%) (in|of|for) \w+",
        r"(type|data type) of \w+",
    ]

    for pattern in column_only_patterns:
        if re.search(pattern, query_lower):
            return {"need_columns": True, "need_dataset": True, "top_k": 3}

    # Both dataset + columns (comparative/exploratory)
    both_patterns = [
        r"correlation between",
        r"relationship",
        r"compare \w+ (and|with|vs)",
        r"all (columns|fields) (that|with|where)",
        r"which columns",
        r"(summarize|summary|overview) (of )?(the )?data",
        r"describe (the )?(entire )?dataset",
    ]

    for pattern in both_patterns:
        if re.search(pattern, query_lower):
            return {"need_columns": True, "need_dataset": True, "top_k": 5}

    # Assume column query
    return {"need_columns": True, "need_dataset": True, "top_k": 5}
