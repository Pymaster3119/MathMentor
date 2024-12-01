import openai
import base64
import json
import openai.types.chat.chat_completion_message

with open("key.txt", "r") as txt:
    client = openai.OpenAI(api_key=txt.read())

class function:
    def __init__ (self, name, description, params, callback, outputname): #Params are in the form {"name": <name>, "type": <type>, "description": <description>}
        self.prompt = {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": {
                },
                "required": [],
                "additionalProperties": False,
            }
        }
        for i in params:
            self.prompt["parameters"]["required"].append(i["name"])
            self.prompt["parameters"]["properties"][i["name"]] = {"type": i["type"], "description": i["description"]}
        self.callback = callback
        self.outputname = outputname
        self.name = name
        self.description = description
        self.params = params
        


#Functions based on https://platform.openai.com/docs/guides/function-calling
def run_query(gpt_model = "gpt-4o-mini", system_text = "", user_prompt = "", image_fname = None, messages = None, functions = None, isfunctioncall = False, returnmessages = False):
    global client

    #Build messages list
    if messages == None or len(messages) == 0:
        messages = [{"role": "system", "content": system_text}]
    elif not isfunctioncall:
        #Remove system text to reduce textcollision
        for i in messages:
            if not isinstance(i, openai.types.chat.chat_completion_message.ChatCompletionMessage) and i["role"] == "system":
                messages.remove(i)
        messages.insert(0, {"role": "system", "content": system_text})

    #Add user prompt, with image if applicable
    if image_fname != None and not isfunctioncall:
        with open(image_fname, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": user_prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"
                    }
                },
            ]
        })
    elif not isfunctioncall:
        messages.append({"role":"user","content":user_prompt})

    #Assemble functions if needed
    if functions != None:
        tools = []
        for i in functions:
            tools.append({"type": "function", "function": i.prompt})
    else:
        tools = None
    #Run model
    try:
        if tools == None:
            response = client.chat.completions.create(
                model=gpt_model,
                messages=messages,
                temperature=0,
                max_tokens=1000,
            )
        else:
            response = client.chat.completions.create(
                model=gpt_model,
                messages=messages,
                temperature=0,
                max_tokens=1000,
                tools= tools
            )
        assistant_response = response
    except openai.OpenAIError as e:
        print(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"

    
    if assistant_response.choices[0].finish_reason != "function_call" and assistant_response.choices[0].finish_reason != "tool_calls":
        messages.append({"role":"assistant", "content":assistant_response.choices[0].message.content.strip()})
        if returnmessages:
            return (assistant_response.choices[0].message.content.strip(), messages)
        else:
            return assistant_response.choices[0].message.content.strip()
    else:
        tool_call = assistant_response.choices[0].message.tool_calls[0]
        arguments = json.loads(tool_call.function.arguments)

        functionidentified = False
        for i in functions:
            if i.name == tool_call.function.name and not functionidentified:
                functionidentified = True
                args = {}
                for j in i.params:
                    args [j["name"]] = arguments.get(j["name"])
                output = i.callback(**args)
                args[i.outputname] = output
                function_call_result_message = {
                    "role": "tool",
                    "content": json.dumps(args),
                    "tool_call_id": response.choices[0].message.tool_calls[0].id
                }      
        if not functionidentified:
            raise Exception("Smth went wrong. Check ur functions sir")
        messages.append(response.choices[0].message)
        messages.append(function_call_result_message)
        if output == "Saved Image":
            with open("static/result.png", "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    },
                ]
            })
        return run_query(gpt_model, system_text, user_prompt, image_fname, messages, functions, False)

