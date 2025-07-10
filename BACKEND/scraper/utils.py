def match_keywords(text: str, keywords: list[str]) -> list[str]:
    matches = []
    lower_text = text.lower()
    for kw in keywords:
        if kw.lower() in lower_text:
            matches.append(kw)
    return matches
