import transformers
import torch
import time

model_id = "meta-llama/Llama-3.1-8B-Instruct"
device = "mps" if torch.backends.mps.is_available() else "cpu"

pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
)

messages = [
    {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
    {"role": "user", "content": "Write a 1000 word essay on pirate's booty."},
]

# Pre-tokenize the messages
tokenized_messages = [pipeline.tokenizer(message["content"], return_tensors="pt").to(device) for message in messages]

terminators = [
    pipeline.tokenizer.eos_token_id,
    pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
]


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
        batch_size=1024,
        num_return_sequences=1
    )
    print(outputs[0]["generated_text"][-1])
    print(f"Time taken: {time.time()-starttime}")