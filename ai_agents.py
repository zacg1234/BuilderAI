from openai import OpenAI
import os
import json
from tools import (
    create_file, read_file, create_folder,
    trigger_engineer, trigger_product,
    trigger_architect, log, insert_before_substring, insert_after_substring, tools
)
from prompts import (product_owner_prompt, system_architect_prompt, software_engineer_prompt, system_architect_qa_prompt)   
from logger import write_log_entry


class AIAgent:

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def call_function(self, function_name, args):
        if function_name == "create_file":
            return create_file(args["path"], args["content"])
        
        elif function_name == "log":
            return log(self.name, args["content"])
        
        elif function_name == "insert_before_substring":
            return insert_before_substring(args["path"], args["substring"], args["additional_content"])
        
        elif function_name == "insert_after_substring":
            return insert_after_substring(args["path"], args["substring"], args["additional_content"])
        
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
            {"role": "system", "content": f"You are {self.name}. {self.description}"},
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
            write_log_entry(f"[{self.name}] Job Finished? {follow_up.output_text}")
            if 'Yes' in follow_up.output_text:
                working = False
                write_log_entry(f"[{self.name}] Job Finished!")
                return "AI Agent said: I am done!"
            memory.append({"role": "user", "content": "Continue with your task by using the provided tools."})
    # run()
# AIAgent Class


class AIAgentFactory:
    @staticmethod
    def get_architect() -> AIAgent:
        return AIAgent("Architect", system_architect_prompt)
    
    @staticmethod
    def get_architect_qa() -> AIAgent:
        return AIAgent("Architect QA", system_architect_qa_prompt)
    @staticmethod
    def get_engineer() -> AIAgent:
        return AIAgent("Engineer", software_engineer_prompt)
        
    @staticmethod
    def get_product() -> AIAgent:
        return AIAgent("Product", product_owner_prompt)