from openai import OpenAI
import os
import json
from tools import (
    create_file, read_file, create_folder,
    trigger_engineer, trigger_product,
    trigger_architect, tools
)
from logger import write_log_entry


class AIAgent:

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def call_function(self, function_name, args):
        if function_name == "create_file":
            return create_file(args["path"], args["content"])
        
        elif function_name == "read_file":
            return read_file(args["path"])
        
        elif function_name == "create_folder":
            return create_folder(args["path"])
        
        elif function_name == "trigger_engineer":
            return trigger_engineer(self.name, args["prompt"], AIAgentFactory.get_engineer())
        
        elif function_name == "trigger_product":
            return trigger_product(self.name, args["prompt"], AIAgentFactory.get_product())
        
        elif function_name == "trigger_architect":
            return trigger_architect(self.name, args["prompt"], AIAgentFactory.get_architect())
        


    def run(self, prompt):
        write_log_entry(f"[{self.name}] PROMPT: {prompt}")
        memory = [
            {"role": "system", "content": f"You are {self.name}, {self.description}."},
            {"role": "user", "content": prompt}
        ]
        working = True
        while working:
            response = self.client.responses.create(
                model="gpt-4.1",
                input=memory,
                tools=tools,
            )
            
            write_log_entry(f"[{self.name}] MODEL RESPONSE: {response.output}")
            
            for tool_call in response.output:
                func_name = tool_call.name
                args = json.loads(tool_call.arguments)

                write_log_entry(f"[{self.name}] TOOL_CALL: {func_name} {args}")
                result = self.call_function(func_name, args)
                write_log_entry(f"[{self.name}] TOOL_RESULT: {result}")

                memory.append(tool_call)
                memory.append({  
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": str(result)
                })

            # print(memory)
            memory.append({"role": "user", "content": "Did you finish your task? Answer with 'Yes' or 'No'."})
            follow_up = self.client.responses.create(
                model="gpt-4.1",
                input=memory
            )
            memory.append({
                "role": "assistant",
                "content": follow_up.output_text
            })
            write_log_entry(f"[{self.name}] Task Finished? {follow_up.output_text}")
            if follow_up.output_text.strip() == 'Yes':
                working = False
                return "AI Agent said: I am done!"
            memory.append({"role": "user", "content": "Check to see if you are finished, or continue with your task by using the provided tools."})
    # run()
# AIAgent Class


class AIAgentFactory:
    @staticmethod
    def get_engineer() -> AIAgent:
        return AIAgent("Engineer", """a Software Engineer. 
            Your job is to look at the file called tasks.txt and execute the tasks one at a time. Do one task at a time and then call yourself with a tool to do the next task.
            If you need to ask a question, ask the Architect agent.
            Once all tasks are done do not do anything else""")
        
    @staticmethod
    def get_product() -> AIAgent:
        return AIAgent("Product", """a Product Owner. 
            Your job is to take the user input and create a comprehensive product requirements document in a file called requirements.txt. 
            Once this file is created trigger the the Architect agent using a tool. Only after the architect is called are you done""")
        
    @staticmethod
    def get_architect() -> AIAgent:
        return AIAgent("Architect", """a System Architect. 
            Your job is to read requirements.txt that contains product requirements and to design an application to fullfil those requierments. 
            Then create a list of tasks for your engineers to execute step by step in the file called tasks.txt. 
            Using the file that you created trigger the Engineer agent using a tool to do one task one at a time - repeat until all tasks are done. you are not done until the engineer does all tasks""")