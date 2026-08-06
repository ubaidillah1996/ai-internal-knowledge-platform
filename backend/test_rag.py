from app.services.rag import ask_question


response = ask_question(
    "How many annual leave days do employees receive?"
)


print("\nANSWER:")
print(response["answer"])


print("\nSOURCES:")

for source in response["sources"]:
    print("----------------")
    print(source["content"][:200])