import re

def needs_history(question: str) -> bool:

    reference_words = [

        "it",
        "its",
        "they",
        "them",
        "their",
        "this",
        "that",
        "these",
        "those",
        "above",
        "previous",
        "earlier",
        "mentioned"

    ]


    words = re.findall(
        r"\b\w+\b",
        question.lower()
    )

    for word in reference_words:

        if word in words:

            return True