import re

def normalize(text: str):
    return re.sub(r"\s+", " ", str(text)).strip().lower()
