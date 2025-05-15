from openai import OpenAI
from dotenv import load_dotenv
from ai_agents import AIAgentFactory
from logger import delete_log_file
from utils import reset_output_folder
from logger import write_log_entry
from utils import output_folder_path
import concurrent.futures


load_dotenv()

def run_engineers_for_tasks():
    # Read tasks from tasks.txt
    with open(f"{output_folder_path}/tasks.txt", "r") as f:
        tasks = [line.strip() for line in f if line.strip()]

    def run_engineer_for_task(task):
        engineer = AIAgentFactory.get_engineer()
        engineer.run("Task: " + task)

    # Run each engineer asynchronously
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_engineer_for_task, task) for task in tasks]
        # Wait for all engineers to finish
        concurrent.futures.wait(futures)

    write_log_entry("[System] All engineer tasks completed.")

# Command-line interaction
def run():
    reset_output_folder()
    delete_log_file()

    print("🧠 AI Agent Prototype Started")
    user_prompt = input("\nWhat are we building today? ").strip()

    # Provide the agent with more context
    AIAgentFactory.get_product().run(user_prompt)
    AIAgentFactory.get_architect().run("")
    AIAgentFactory.get_architect_qa().run("")
    run_engineers_for_tasks()

       
if __name__ == "__main__":
    run()
