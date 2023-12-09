import json
from difflib import get_close_matches
import os

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, 'knowledge_base.json')

def load_knowledge(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as file:
            data: dict = json.load(file)
        return data
    except FileNotFoundError:
        # If the file doesn't exist, return an empty dictionary
        return {"questions": []}

def save_knowledge(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def answer(user_input: str, questions: list[str]) -> str|None:
    matches: list = get_close_matches(user_input, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def learn(question: str, knowledge_base: dict) -> str|None:
    for knowledge in knowledge_base["questions"]:
        if knowledge["question"] == question:
            return knowledge["answer"]

def chat_with_bot():
    knowledge_base: dict = load_knowledge(file_path)

    while True:
        user_input: str = input('You: ')

        if user_input.lower() == 'quit':
            break

        match: str | None = answer(user_input, [knowledge["question"] for knowledge in knowledge_base["questions"]])

        if match:
            response: str = learn(match, knowledge_base)
            print(f'Bot: {response}')
        else:
            print('Bot: I don\'t know the answer. Enter the possible answer for that conversation.')
            fresh_knowledge: str = input('Enter the answer or type "skip" to skip: ')

            if fresh_knowledge.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": fresh_knowledge})
                save_knowledge(file_path, knowledge_base)
                print("Bot: Thanks for the new information")

if __name__ == '__main__':
    chat_with_bot()
