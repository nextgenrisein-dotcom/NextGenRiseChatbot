from chatbot import ask


while True:

    question = input("\nAsk NextGen Rise AI: ")

    if question.lower() == "exit":
        break

    answer = ask(question)

    print("\nAssistant:")
    print(answer)