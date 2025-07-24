from smart_agent import SmartAgent

with open("IntroToLLm/context_prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

smartAgent = SmartAgent("gemma3:1b", system_prompt)

question = input("question? : ").strip()

while question != "/pa":
    if question != "":
        answer_text = smartAgent.chat(question)
        print(answer_text)

    question = input("question? : ").strip()
