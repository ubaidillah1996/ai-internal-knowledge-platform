import ollama


response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "user",
            "content": "Explain artificial intelligence in one sentence."
        }
    ]
)


print(
    response["message"]["content"]
)