from transformers import pipeline
import torch
import re
import time
import os
import json

def sendmsgs(systemtext, chatprompt, return_history=False, user_id=""):
    print(user_id)
    if not os.path.isdir(f"LLamaInteraction/LLMInput_{user_id}"):
        os.mkdir(f"LLamaInteraction/LLMInput_{user_id}")
        with open(f"LLamaInteraction/LLMInput_{user_id}/FullHistory.json", "w") as txt:
            txt.write("")
        with open(f"LLamaInteraction/LLMInput_{user_id}/Output", "w") as txt:
            txt.write("")
    with open(f"LLamaInteraction/LLMInput_{user_id}/SystemText", "w") as txt:
        txt.write(systemtext)
    with open(f"LLamaInteraction/LLMInput_{user_id}/Input", "w") as txt:
        txt.write(chatprompt)
    while True:
        with open(f"LLamaInteraction/LLMInput_{user_id}/Output", "r") as txt:
            output = txt.read()
        if output != "":
            with open(f"LLamaInteraction/LLMInput_{user_id}/Output", "w") as txt:
                txt.write("")
            if not return_history:
                return output
            else:
                history = [{"role":"system", "content":systemtext}, {"role":"user", "content":chatprompt}, {"role":"assistant", "content":output}]
                return (output, history)

def send_msgs_history(messages, user_id):
    if not os.path.isdir(f"LLamaInteraction/LLMInput_{user_id}"):
        os.mkdir(f"LLamaInteraction/LLMInput_{user_id}")
        with open(f"LLamaInteraction/LLMInput_{user_id}/SystemText", "w") as txt:
            txt.write("")
        with open(f"LLamaInteraction/LLMInput_{user_id}/Input", "w") as txt:
            txt.write("")
        with open(f"LLamaInteraction/LLMInput_{user_id}/Output", "w") as txt:
            txt.write("")
    with open(f"LLamaInteraction/LLMInput_{user_id}/FullHistory.json", "w") as txt:
        txt.write(json.dumps(messages))
    while True:
        with open(f"LLamaInteraction/LLMInput_{user_id}/Output", "r") as txt:
            output = txt.read()
        if output != "":
            with open(f"LLamaInteraction/LLMInput_{user_id}/Output", "w") as txt:
                txt.write("")
            return output