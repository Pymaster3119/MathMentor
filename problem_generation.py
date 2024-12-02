import gpt_interaction
import re

with open("problem_generator_system_text.txt", "r") as txt:
    system_text = txt.read()

#Multiple Choice
def multiple_choice(question, answer_a, answer_b, answer_c, answer_d):
    print("----------------------------------")
    print(f"question: {question}")
    print(f"a. {answer_a}")
    print(f"b. {answer_b}")
    print(f"c. {answer_c}")
    print(f"d. {answer_d}")
    answer = input("Answer:")
    print("----------------------------------")
    return answer

multiple_choice_function = gpt_interaction.function(
    name="multiple_choice", 
    description="The function used to create a multiple choice question", 
    params=[
        {"name": "question", "type": "string", "description": "The question asked"},
        {"name": "answer_a", "type": "string", "description": "The first answer choice (option A)"},
        {"name": "answer_b", "type": "string", "description": "The second answer choice (option B)"},
        {"name": "answer_c", "type": "string", "description": "The third answer choice (option C)"},
        {"name": "answer_d", "type": "string", "description": "The last answer choice (option D)"}
    ],
    callback=multiple_choice,
    outputname="answer"
)

#Word problems
def word_problem(question):
    print("----------------------------------")
    print(f"question: {question}")
    answer = input("Answer:")
    print("----------------------------------")
    return answer

word_problem_function = gpt_interaction.function(
    name="word_problem", 
    description="The function used to create a word problem", 
    params=[{"name": "question", "type": "string", "description": "The question asked"}],
    callback=word_problem,
    outputname="User Answer"
)


#Create problems
correct = 0

messages = []
def create_question(prompt):
    global messages, correct
    result = gpt_interaction.run_query(system_text=system_text, user_prompt=prompt,messages=messages, functions=[multiple_choice_function, word_problem_function])
    if "orrect" in result:
        correct += 1
    #TODO: Make the UI
    print(result)
    work = re.findall(r"'''work(.*?)'''", result, re.DOTALL)
    print(work)

create_question("AP Precalculus")