from transformers import pipeline
import torch
import time
import json
import glob
import os


model_id = "meta-llama/Llama-3.2-3B-Instruct"
device = "mps" if torch.backends.mps.is_available() else "cpu"

pipeline = pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
)

while True:
    #Filter through all folders with glob
    folders = glob.glob("/Users/aditya/Desktop/InProgress/MathMentor/LLamaInteraction/LLMInput_*")
    for folder in folders:
        if os.path.isdir(folder):
            # Deal with single input/system text
            with open(f"{folder}/Input", "r") as txt:
                input = txt.read()
            with open(f"{folder}SystemText", "r") as txt:
                systemtext = txt.read()
            if input != "":
                print("Reading single input")
                starttime = time.time()
                messages = [
                    {"role": "system", "content": systemtext},
                    {"role": "user", "content": input},
                ]

                # Tokenize messages
                tokenized_messages = [pipeline.tokenizer(message["content"], return_tensors="pt").to(device) for message in messages]

                terminators = [
                    pipeline.tokenizer.eos_token_id,
                    pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
                ]

                #Run the model
                with torch.no_grad():
                    print("Start generating...")
                    starttime = time.time()
                    outputs = pipeline(
                        messages,
                        max_new_tokens=1024,
                        eos_token_id=terminators,
                        do_sample=True,
                        temperature=0.6,
                        top_p=0.9,
                        batch_size=1024
                    )
                with open(f"{folder}/Output", "w") as txt:
                    txt.write(outputs[0]["generated_text"][-1]["content"])
                with open(f"{folder}/Input", "w") as txt:
                    txt.write("")
                
                endtime = time.time()
                print("Time taken for a single input: " + str(endtime - starttime))

            # Deal with the full history
            with open(f"{folder}FullHistory.json", "r") as txt:
                history = txt.read()
            if history != "":
                print("Reading full history")
                starttime = time.time()
                history = json.loads(history)

                # Tokenize messages
                tokenized_messages = [pipeline.tokenizer(message["content"], return_tensors="pt").to(device) for message in messages]

                terminators = [
                    pipeline.tokenizer.eos_token_id,
                    pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
                ]

                #Run the model
                with torch.no_grad():
                    print("Start generating...")
                    starttime = time.time()
                    outputs = pipeline(
                        messages, 
                        max_new_tokens=1024,
                        eos_token_id=terminators,
                        do_sample=True,
                        temperature=0.6,
                        top_p=0.9,
                        batch_size=1024
                    )
                with open(f"{folder}/Output", "w") as txt:
                    txt.write(outputs[0]["generated_text"][-1]["content"])
                with open(f"{folder}/FullHistory.json", "w") as txt:
                    txt.write("")
                endtime = time.time()
                print("Time taken for a full history: " + str(endtime - starttime))

    time.sleep(0.1)