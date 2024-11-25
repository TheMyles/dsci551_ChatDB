from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.util import ngrams

QUERY_PATTERNS = {
    "EXAMPLE": ["example", "examples", "sample", "instance", "demo", "case"],
    "SHOW": ['tables', 'describe', 'database'],
    "UPLOAD": ["upload", "add", "insert", "import", "save", "load", "store"],
    "SELECT": ["select", "columns", "fields", "retrieve", "get", "show", "fetch", "extract",
               "display", "list", "view", "pick", "choose", "read", "query"],
    "AGGREGATE": ["many", "sum", "average", "mean", "count", "total", "maximum", "minimum",
                  "min", "max", "avg", "median", "aggregate", "statistics", "metrics"],
    "GROUP BY": ["group by", "aggregate", "group", "grouping", "each", "total", "categorize",
                 "partition", "classify", "segment", "cluster", "bucket", 'grouped'],
    "HAVING": ["having", "condition", "filter", "over", "under", "less", "greater", "limit", 'more',
               "range", "restrict", "criteria", "threshold", "constraint", "above", "below"],
    "ORDER BY": ["order by", "sort", "ascending", "descending", "rank", "arrange", "prioritize",
                 "sequence", "order", "hierarchy", "top", "bottom", "sorted", "biggest"],
    "WHERE": ["where", "condition", "filter", "over", "under", "less", "greater", "who",
              "which", "that", "criteria", "subset", "find", "limit", "restrict", "search",
              "match", "constraint"],
    "JOIN": ["join", "merge", "combine", "foreign key", "unite", "relate", "link",
             "connect", "associate", "bridge", "union", "inner", "outer", "left", "right"],
    "LIMIT": ['top', 'bottom', 'highest', 'lowest', 'biggest', 'smallest', 'limit'],
    "SQL": ['sql', 'mysql'],
    "MONGODB": ['mongo', 'mongodb', 'nosql']
}

def match_query_pattern(user_input):
    tokens = word_tokenize(user_input.lower())
    tokens = [token for token in tokens if token.isalnum()]  # Remove punctuation
    stop_words = set(stopwords.words('english'))

    for words in QUERY_PATTERNS.values():
        stop_words -= set(words)

    filtered_tokens = [token for token in tokens if token not in stop_words]

    # Detect n-grams (e.g., "group by")
    bigrams = list(ngrams(tokens, 2))
    phrases = [" ".join(bigram) for bigram in bigrams]

    # Match tokens and phrases to query patterns
    detected_types = []
    for query_type, keywords in QUERY_PATTERNS.items():
        for word in filtered_tokens + phrases:
            if word in keywords:
                detected_types.append(query_type)
                break

    # Handle contextual relationships
    if "HAVING" in detected_types and "GROUP BY" not in detected_types:
        detected_types.remove("HAVING")
    
    if "AGGREGATE" in detected_types and "SELECT" in detected_types:
        detected_types.remove("SELECT")
    
    if 'SELECT' not in detected_types and 'AGGREGATE' not in detected_types:
        detected_types.append('SELECT')
    
    return list(set(detected_types))
