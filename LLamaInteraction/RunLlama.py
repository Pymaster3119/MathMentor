from transformers import pipeline
import torch
import re
import time
import os
import json
os.environ["TOKENIZERS_PARALLELISM"] = "true"

model_id = "meta-llama/Llama-3.2-3B-Instruct"

pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

while True:
    #Clear all files
    with open("LLamaInteraction/Input", "w") as txt:
        txt.write("")
    with open("LLamaInteraction/SystemText", "w") as txt:
        txt.write("")
    with open("LLamaInteraction/Output", "w") as txt:
        txt.write("")

    #Deal with single input/system text
    with open("LLamaInteraction/Input", "r") as txt:
        input = txt.read()
    if input != "":
        with open("LLamaInteraction/SystemText", "r") as txt:
            systemtext = txt.read()
        messages = [
            {"role": "system", "content": systemtext},
            {"role": "user", "content": input},
        ]
        outputs = pipe(
            messages,
            max_new_tokens=1024,
        )
        endtime = time.time()
        with open("LLamaInteraction/Output", "w") as txt:
            txt.write(outputs[0]["generated_text"][-1]["content"])

    #Deal with the full history
    with open("LLamaInteraction/FullHistory.json", "r") as txt:
        history = txt.read()
        if history != "":
            history = json.loads(history)
        outputs = pipe(
            messages,
            max_new_tokens=1024,
        )
        with open("LLamaInteraction/Output", "w") as txt:
            txt.write(outputs[0]["generated_text"][-1]["content"])

    time.sleep(0.1)