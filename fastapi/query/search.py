

def parse_query(q: str):
    # Remove punctuation
    q = q.replace(",", "").replace(".", "").replace("!", "").replace("?", "")
    # Split on spaces
    qs = q.split(" ")
    # Lower case
    qs = [x.lower() for x in qs]
    # Remove stop words
    stop_words = ["a", "an", "the", "is", "in", "on", "at", "to", "of", "and", "or", "not", "with", "for", "by", "as", "from", "that", "this", "these", "those", "there", "here", "where", "when", "why", "how", "what", "which", "who", "whom", "whose"]
    qs = [x for x in qs if x not in stop_words]
    return qs