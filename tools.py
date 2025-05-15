import os
from logger import write_log_entry
from utils import output_folder_path

# * Function to edit a portion of a file

  
def create_file(path: str, content: str) -> str:
    full_path = output_folder_path + "/" + path
    if os.path.isfile(full_path):
        os.remove(full_path)
    with open(full_path, "w") as f:
        f.write(content)
    return f"File '{path}' created with this content: \n{content}"

def read_file(path: str) -> str:
    try:
        with open(output_folder_path + "/" +path, "r") as f:
            return f"File at '{path}' contains: \n{f.read()}"
    except FileNotFoundError:
        return "File not found."

def create_folder(path: str) -> str:
    full_path = output_folder_path + "/" + path
    if os.path.isfile(full_path):
        return f"Folder '{path}' created."
    os.makedirs(full_path, exist_ok=True)
    return f"Folder '{path}' created."

def trigger_engineer(my_name: str, prompt: str, engineer) -> str:
    write_log_entry(f"[{my_name} - CALLING Software Engineer] message: {prompt}")
    return engineer.run(f"{my_name} has instructions for you: {prompt}")

def trigger_product(my_name: str, prompt: str, product) -> str:
    write_log_entry(f"[{my_name} - CALLING Product Owner] message: {prompt}")
    return product.run(f"{my_name} has instructions for you: {prompt}")

def trigger_architect(my_name: str, prompt: str, architect) -> str:
    write_log_entry(f"[{my_name} - CALLING System Architect] message: {prompt}")
    return architect.run(f"{my_name} has instructions for you: {prompt}")

tools = [
    {
        "type": "function",
        "name": "create_file",
        "description": "Create a file at a given path with content.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string"},
            },
        "required": ["path", "content"]
        } 
    },

    {
        "type": "function",
        "name": "read_file",
        "description": "Read the contents of a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
            },
            "required": ["path"]
        }
    },
    {
        "type": "function",
        "name": "create_folder",
        "description": "Create a folder at a given path.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
            },
            "required": ["path"]
        }
    },
    {
        "type": "function",
        "name": "trigger_engineer",
        "description": "Communicate with a Software Engineer - either ask him a question or tell him what to do.",
        "parameters": {
            "type": "object",
            "properties": {
                "my_name": {"type": "string"},
                "prompt": {"type": "string"},
            },
            "required": ["my_name", "prompt"]
        }
    },
    {
        "type": "function",
        "name": "trigger_product",
        "description": "Communicate with a Product Owner - either ask him a question or tell him what to do.",
        "parameters": {
            "type": "object",
            "properties": {
                "my_name": {"type": "string"},
                "prompt": {"type": "string"},
            },
            "required": ["my_name", "prompt"]
        }
    },
    {
        "type": "function",
        "name": "trigger_architect",
        "description": "Communicate with a System Architect - either ask him a question or tell him what to do.",
        "parameters": {
            "type": "object",
            "properties": {
                "my_name": {"type": "string"},
                "prompt": {"type": "string"},
            },
            "required": ["my_name", "prompt"]
        }
    }
]
