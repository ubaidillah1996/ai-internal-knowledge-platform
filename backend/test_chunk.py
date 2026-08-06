from app.services.chunking import create_chunks


text = """
AI Internal Knowledge Platform.
This document contains company information.
Employees must follow security policies.
"""


chunks = create_chunks(
    text,
    50
)


for index, chunk in enumerate(chunks):

    print(
        "CHUNK",
        index
    )

    print(chunk)

    print("----------------")