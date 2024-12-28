from transformers import pipeline
import torch
import time
import os
import json
os.environ["TOKENIZERS_PARALLELISM"] = "true"

model_id = "meta-llama/Llama-3.2-3B-Instruct"

pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.float16,
    device_map="auto",
)
while True:
    #Deal with single input/system text
    with open("/Users/aditya/Desktop/InProgress/MathMentor/LLamaInteraction/Input", "r") as txt:
        input = txt.read()
    if input != "":
        print("Reading single input")
        starttime = time.time()
        with open("/Users/aditya/Desktop/InProgress/MathMentor/LLamaInteraction/SystemText", "r") as txt:
            systemtext = txt.read()
        messages = [
            {"role": "system", "content": systemtext},
            {"role": "user", "content": input},
        ]
        outputs = pipe(
            messages,
            max_new_tokens=1024,
        )
        with open("/Users/aditya/Desktop/InProgress/MathMentor/LLamaInteraction/Output", "w") as txt:
            txt.write(outputs[0]["generated_text"][-1]["content"])
        with open("/Users/aditya/Desktop/InProgress/MathMentor/LLamaInteraction/Input", "w") as txt:
            txt.write("")
        with open("/Users/aditya/Desktop/InProgress/MathMentor/LLamaInteraction/SystemText", "w") as txt:
            txt.write("")
        
        endtime = time.time()
        print("Time taken for a single input test: " + str(endtime - starttime))

    #Deal with the full history
    with open("/Users/aditya/Desktop/InProgress/MathMentor/LLamaInteraction/FullHistory.json", "r") as txt:
        
        starttime = time.time()
        history = txt.read()
        if history != "":
            print("Reading full history")
            history = json.loads(history)
            outputs = pipe(
                history,
                max_new_tokens=1024,
            )
            with open("/Users/aditya/Desktop/InProgress/MathMentor/LLamaInteraction/Output", "w") as txt:
                txt.write(outputs[0]["generated_text"][-1]["content"])
            with open("/Users/aditya/Desktop/InProgress/MathMentor/LLamaInteraction/FullHistory.json", "w") as txt:
                txt.write("")
            endtime = time.time()
            print("Time taken for a full history: " + str(endtime - starttime))
    time.sleep(0.1)