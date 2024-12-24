from transformers import pipeline
import torch
import re
import time
import os
import json

os.system("python3 LLamaInteraction/RunLlama.py")

def sendmsgs(systemtext, chatprompt):
    with open("LLamaInteraction/SystemText", "w") as txt:
        txt.write(systemtext)
    with open("LLamaInteraction/Input", "w") as txt:
        txt.write(chatprompt)
    while True:
        with open("LLamaInteraction/Output", "r") as txt:
            output = txt.read()
        if output != "":
            return output

def send_msgs_history(messages):
    with open("LLamaInteraction/FullHistory.json", "w") as txt:
        txt.write(json.dumps(messages))
    while True:
        with open("LLamaInteraction/Output", "r") as txt:
            output = txt.read()
        if output != "":
            return output