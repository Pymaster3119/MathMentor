import gpt_interaction
import re
import json
import time

with open("problem_generator_system_text.txt", "r") as txt:
    system_text = txt.read()

answer = None
answered = False
#Multiple Choice
def multiple_choice(question, answer_a, answer_b, answer_c, answer_d):
    global answer, answered
    with open("question.txt", "w") as txt:
        txt.write(question + "<br><br>")
        txt.write(f"a. {answer_a}<br>b. {answer_b}<br>c. {answer_c}<br>d. {answer_d}")
    answered = False
    while answer == None:
        time.sleep(0.001)
    answerlocal = str(answer)
    answer = None
    answered = True
    return answerlocal
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
    outputname="User Answer"
)

#Word problems
def word_problem(question):
    global answer
    with open("question.txt", "w") as txt:
        txt.write(question)
    
    while answer == None:
        time.sleep(0.001)
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
    result = gpt_interaction.run_query(gpt_model="gpt-4o", system_text=system_text, user_prompt=prompt,messages=messages, functions=[multiple_choice_function, word_problem_function])
    print(result)
    if "orrect" in result:
        correct += 1
    #TODO: Make the UI
    work = re.findall(r"```work(.*?)```", result, re.DOTALL)[0]
    print(work)
    with open("problem_result.json", "w") as file:
        json.dump(
            {"result":"correct" if correct else "incorrect", "work":work},
            file, indent = 4)