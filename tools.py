import os
from logger import write_log_entry
from utils import output_folder_path

# * Function to edit a portion of a file

  
def create_file(path: str, content: str) -> str:
    full_path = output_folder_path + "/" + path
    os.makedirs(os.path.dirname(full_path), exist_ok=True)  # Ensure parent dirs exist
    if os.path.isfile(full_path):
        os.remove(full_path)
    with open(full_path, "w") as f:
        f.write(content)
    return f"File '{path}' created with this content: \n{content}"

def log(my_name: str, content: str) -> str:
    log_content = f"LOGGING {my_name}: {content}"
    write_log_entry("LOGGING" + my_name +  ": " + content)
    return f"The folowing was logged: {log_content}"

def insert_after_substring(path: str, substring: str, additional_content: str) -> str:
    full_path = output_folder_path + "/" + path
    try:
        with open(full_path, "r") as f:
            content = f.read()
        index = content.find(substring)
        if index == -1:
            return f"Substring '{substring}' not found in '{path}'."
        insert_pos = index + len(substring)
        new_content = content[:insert_pos] + additional_content + content[insert_pos:]
        with open(full_path, "w") as f:
            f.write(new_content)
        return f"Inserted content after '{substring}' in '{path}'."
    except FileNotFoundError:
        return f"File '{path}' not found."
    except Exception as e:
        return f"Error: {e}"
    
def insert_before_substring(path: str, substring: str, additional_content: str) -> str:
    full_path = output_folder_path + "/" + path
    try:
        with open(full_path, "r") as f:
            content = f.read()
        index = content.find(substring)
        if index == -1:
            return f"Substring '{substring}' not found in '{path}'."
        new_content = content[:index] + additional_content + content[index:]
        with open(full_path, "w") as f:
            f.write(new_content)
        return f"Inserted content before '{substring}' in '{path}'."
    except FileNotFoundError:
        return f"File '{path}' not found."
    except Exception as e:
        return f"Error: {e}"

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
        "name": "log",
        "description": "Log a message with the agent's name.",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {"type": "string"},
            },
            "required": ["content"]
        }
    },
    {
        "type": "function",
        "name": "insert_after_substring",
        "description": "Insert additional content into a file immediately after the first occurance of a given substring. So choose the shortest unique substring to append after",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "substring": {"type": "string"},
                "additional_content": {"type": "string"},
            },
            "required": ["path", "substring", "additional_content"]
        }
    },
    {
        "type": "function",
        "name": "insert_before_substring",
        "description": "Insert additional content into a file immediately before the first occurrence of a given substring. So choose the shortest unique substring to prepend before.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "substring": {"type": "string"},
                "additional_content": {"type": "string"},
            },
            "required": ["path", "substring", "additional_content"]
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
                "prompt": {"type": "string"},
            },
            "required": [ "prompt"]
        }
    },
    {
        "type": "function",
        "name": "trigger_product",
        "description": "Communicate with a Product Owner - either ask him a question or tell him what to do.",
        "parameters": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string"},
            },
            "required": ["prompt"]
        }
    },
    {
        "type": "function",
        "name": "trigger_architect",
        "description": "Communicate with a System Architect - either ask him a question or tell him what to do.",
        "parameters": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string"},
            },
            "required": ["prompt"]
        }
    }
]
