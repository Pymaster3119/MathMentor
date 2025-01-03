from transformers import pipeline
import torch
import time
import json


device = torch.device("mps")
torch.compile()
torch.set_num_threads(64)

model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

# This is the pipeline that will be used to generate the responses
pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.bfloat16,
    device_map=device,
    max_length=1024,
    num_return_sequences=1,
    pad_token_id=50256,
    
)


def find_max_batch_size(pipe, messages, start=32, end=999):
    for batch_size in range(end, start, -1):
        try:
            starttime = time.time()
            pipe(messages, batch_size=batch_size)
            endtime = time.time()
            print("Time taken for batch size " + str(batch_size) + ": " + str(endtime - starttime))
            return batch_size
        except RuntimeError as e:
            print("Error with batch size " + str(batch_size) + ": " + str(e))
    return "No batch size found"

print(find_max_batch_size(pipe, [{"role": "system", "content": "You are a friendly assistant."}, {"role": "user", "content": "Write me a biography of Joe Arridy."}]))