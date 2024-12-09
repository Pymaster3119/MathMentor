import gpt_interaction
import re
import json
import time
import os
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output

with open("problem_generator_system_text.txt", "r") as txt:
    generator_system_text = txt.read()

with open("problem_checker_system_text.txt", "r") as txt:
    checker_system_text = txt.read()

with open("correctgpt_system_text.txt", "r") as txt:
    correctgpt_system_text = txt.read()

answer = None
answered = False
questiong = None

#Word problems
def word_problem(question):
    global answer, questiong
    with open("question.txt", "w") as txt:
        txt.write(question)
    questiong = question
    
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

#Checker
def check(code):
    code.replace("\\n", "\n")
    shell = InteractiveShell.instance()
    with capture_output() as captured:
        shell.run_cell(code)
    output = captured.stdout.strip()
    print(type(output))
    return output
checker_function = gpt_interaction.function(
    name="python_eval", 
    description="The function used to run code in python", 
    params=[{"name": "code", "type": "string", "description": "The code to be run"}],
    callback=check,
    outputname="User Answer"
)

#Create problems
def create_question(prompt):
    global answered, questiong
    gpt_interaction.run_query(gpt_model="gpt-4o", system_text=generator_system_text, user_prompt=prompt,messages=[], functions=[word_problem_function], callGPTafterfunction=False)
    while answer == None:
        time.sleep(0.001)
    checker_messages = []
    _, checker_messages = gpt_interaction.run_query(gpt_model="gpt-4o", system_text=checker_system_text, messages=checker_messages, user_prompt=questiong, functions=[checker_function], returnmessages=True)
    result = gpt_interaction.run_query(gpt_model="gpt-4o", system_text=checker_system_text, messages=checker_messages, user_prompt="Great! Now, do the calculations and give me an answer", functions=[checker_function], returnmessages=False)
    work = re.findall(r"```work(.*?)```", result, re.DOTALL)[0]
    correctanswer = re.findall(r"ANSWER: (.*?)", result, re.DOTALL)[0]

    print(work)

    correctness = gpt_interaction.run_query(gpt_model="gpt-4o",system_text=correctgpt_system_text, user_prompt=f"answer1: {answer}\nanswer2: {correctanswer}")
    print(f"answer1: {answer}\nanswer2: {correctanswer}")
    print(correctness)
    with open("problem_result.json", "w") as file:
        json.dump(
            {"result":correctness, "work":work},
            file, indent = 4)
        answered = True