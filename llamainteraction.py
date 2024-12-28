from transformers import pipeline
import torch
import re
import time
import os
import json

def sendmsgs(systemtext, chatprompt, return_history=False):
    print("hehehehehehehehehre")
    with open("LLamaInteraction/SystemText", "w") as txt:
        txt.write(systemtext)
    with open("LLamaInteraction/Input", "w") as txt:
        txt.write(chatprompt)
    while True:
        with open("LLamaInteraction/Output", "r") as txt:
            output = txt.read()
        if output != "":
            print("heheheheeeheeheeheeeereere")
            with open("LLamaInteraction/Output", "w") as txt:
                txt.write("")
            if not return_history:
                return output
            else:
                history = [{"role":"system", "content":systemtext}, {"role":"user", "content":chatprompt}, {"role":"assistant", "content":output}]
                return (output, history)

def send_msgs_history(messages):
    with open("LLamaInteraction/FullHistory.json", "w") as txt:
        txt.write(json.dumps(messages))
    while True:
        with open("LLamaInteraction/Output", "r") as txt:
            output = txt.read()
        if output != "":
            with open("LLamaInteraction/Output", "w") as txt:
                txt.write("")
            return output