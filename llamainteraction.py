from transformers import pipeline
import torch
import re
import time
import os
os.environ["TOKENIZERS_PARALLELISM"] = "true"

model_id = "meta-llama/Llama-3.2-3B-Instruct"

pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

starttime = time.time()


endtime = time.time()
print(endtime-starttime)


def sendmsgs(systemtext, chatprompt):
    print("Hjere")
    starttime = time.time()
    messages = [
        {"role": "system", "content": systemtext},
        {"role": "user", "content": chatprompt},
    ]
    outputs = pipe(
        messages,
        max_new_tokens=1024,
    )
    print(outputs)
    endtime = time.time()
    print(endtime-starttime)
    return outputs[0]["generated_text"][-1]["content"]

sendmsgs("hi", "hi")

def send_msgs_history(messages):
    outputs = pipe(
        messages,
        max_new_tokens=1024,
    )
    print(outputs)
    endtime = time.time()
    print(endtime-starttime)
    return outputs[0]["generated_text"][-1]["content"]