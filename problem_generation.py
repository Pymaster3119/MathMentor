import gpt_interaction
import json
import time
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output
import llamainteraction

with open("problem_generator_system_text.txt", "r") as txt:
    generator_system_text = txt.read()

with open("problem_checker_system_text.txt", "r") as txt:
    checker_system_text = txt.read()

with open("correctgpt_system_text.txt", "r") as txt:
    correctgpt_system_text = txt.read()

user_answers = {}
user_answered = {}

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

def set_answer(user_id, answer):
    user_answers[user_id] = answer

#Create problems
def create_question(prompt, previous_question=None, status=None, user_id=None):
    with open(f"{user_id}_question.txt", "w") as txt:
        txt.write("")
    with open(f"{user_id}_problem_result.json", "w") as txt:
        txt.write("")
    user_answered[user_id] = False

    #Generate the question
    print(previous_question)
    if previous_question == None or status == "different":
        question = llamainteraction.sendmsgs(generator_system_text, prompt, user_id=user_id)
    else:
        if status == "similar":
            messages = [{"role": "system", "content": generator_system_text}, {"role": "user", "content": prompt}, {"role": "assistant", "content": previous_question}, {"role": "user", "content": "Give me a similar question"}]
        elif status == "easier":
            messages = [{"role": "system", "content": generator_system_text}, {"role": "user", "content": prompt}, {"role": "assistant", "content": previous_question}, {"role": "user", "content": "Give me an easier question"}]
        elif status == "harder":
            messages = [{"role": "system", "content": generator_system_text}, {"role": "user", "content": prompt}, {"role": "assistant", "content": previous_question}, {"role": "user", "content": "Give me a harder question"}]
        question = llamainteraction.send_msgs_history(messages, user_id=user_id)
    
    with open(f"{user_id}_question.txt", "w") as txt:
        txt.write(question)
    
    while user_id not in user_answers:
        time.sleep(0.001)

    answer = user_answers[user_id]

    #Check the answer
    checker_messages = []
    _, checker_messages = llamainteraction.sendmsgs(systemtext=checker_system_text, chatprompt=question, return_history=True, user_id=user_id)
    print(checker_messages)
    #Deal with the functions
    while True:
        result = llamainteraction.send_msgs_history(checker_messages, user_id=user_id)
        checker_messages.append({"role": "assistant", "content": result})
        print(result)
        try:
            result_json = json.loads(result)
            function_name = result_json.get("function_name")

            if function_name == "submit_answer":
                work = result_json.get("work")
                correctanswer = result_json.get("correctanswer")

                if work is None:
                    checker_messages.append({"role": "functions", "content": "Error: Work parameter is missing"})
                    continue

                if correctanswer is None:
                    checker_messages.append({"role": "functions", "content": "Error: Correct answer parameter is missing"})
                    continue

                correctanswer = correctanswer
                work = work
                break

            elif function_name == "python_eval":
                code = result_json.get("code")

                if code is None:
                    checker_messages.append({"role": "functions", "content": "Error: Code parameter is missing"})
                    continue

                try:
                    checker_messages.append({"role": "functions", "content": checker_function(code)})
                except:
                    checker_messages.append({"role": "functions", "content": "Error: Invalid code"})

            else:
                checker_messages.append({"role": "functions", "content": "Error: Invalid function name"})

        except json.JSONDecodeError:
            checker_messages.append({"role": "functions", "content": "Error: Invalid JSON"})
        except KeyError:
            checker_messages.append({"role": "functions", "content": "Error: Function name is missing"})
    
    print(work)
    correctness = llamainteraction.sendmsgs(correctgpt_system_text, f"question: {question}\nanswer1: {answer}\nanswer2: {correctanswer}", user_id = user_id)
    correctness = "Correct!" if "correct" in correctness.lower() else ("Incorrect!" if "incorrect" in correctness.lower() else correctness)
    with open(f"{user_id}_problem_result.json", "w") as file:
        json.dump(
            {"result":correctness, "work":work},
            file, indent = 4)
        user_answered[user_id] = True