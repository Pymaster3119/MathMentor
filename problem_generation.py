
import gpt_interaction
import re
import json
import time
import os
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output
import llamainteraction
import concurrent.futures

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

#Submit Work
correctanswerg = None
workg = None
def submitwork(correctanswer, work):
    global correctanswerg, workg
    correctanswerg = correctanswer
    workg = work
submit_function = gpt_interaction.function(
    name="submit_answer", 
    description="The function used to submit your final answer and work", 
    params=[{"name": "work", "type": "string", "description": "The work leading up to your answer, neatly summarized"}, {"name": "correctanswer", "type": "string", "description": "The correct answer"}],
    callback=submitwork,
    outputname="User Answer"
)

#Create problems
def create_question(prompt, previous_question=None, status=None):
    with open("question.txt", "w") as txt:
        txt.write("")
    with open("problem_result.json", "w") as txt:
        txt.write("")
    global answered, questiong
    questiong = None

    #Generate the question
    if previous_question == None or status == "different":
        print("Heheeheeere")
        question = llamainteraction.sendmsgs(generator_system_text, prompt)
    else:
        if status == "similar":
            messages = [{"role": "system", "content": generator_system_text}, {"role": "user", "content": prompt}, {"role": "assistant", "content": previous_question}, {"role": "user", "content": "Give me a similar question"}]
        elif status == "easier":
            messages = [{"role": "system", "content": generator_system_text}, {"role": "user", "content": prompt}, {"role": "assistant", "content": previous_question}, {"role": "user", "content": "Give me an easier question"}]
        elif status == "harder":
            messages = [{"role": "system", "content": generator_system_text}, {"role": "user", "content": prompt}, {"role": "assistant", "content": previous_question}, {"role": "user", "content": "Give me a harder question"}]
        question = llamainteraction.send_msgs_history(messages)
    word_problem(question)
    while answer == None:
        time.sleep(0.001)

    #Check the answer
    checker_messages = []
    _, checker_messages = gpt_interaction.run_query(gpt_model="gpt-4o", system_text=checker_system_text, messages=checker_messages, user_prompt=questiong, functions=[checker_function, submit_function], returnmessages=True)
    result = gpt_interaction.run_query(gpt_model="gpt-4o", system_text=checker_system_text, messages=checker_messages, user_prompt="Great! Now, do the calculations and give me an answer", functions=[checker_function, submit_function], returnmessages=False)
    work = workg
    correctanswer = correctanswerg
    print(work)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(llamainteraction.sendmsgs,correctgpt_system_text, f"question: {question}\nanswer1: {answer}\nanswer2: {correctanswer}")]
    for future in concurrent.futures.as_completed(futures):
        correctness = future.result()
    print(correctness)
    correctness = "Correct!" if "correct" in correctness.lower() else ("Incorrect!" if "incorrect" in correctness.lower() else correctness)
    with open("problem_result.json", "w") as file:
        json.dump(
            {"result":correctness, "work":work},
            file, indent = 4)
        answered = True
