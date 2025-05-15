from openai import OpenAI
from dotenv import load_dotenv
from ai_agents import AIAgentFactory
from logger import delete_log_file
from utils import reset_output_folder


load_dotenv()

# Command-line interaction
def run():
    reset_output_folder()
    delete_log_file()

    print("🧠 AI Agent Prototype Started")
    user_prompt = input("\nWhat are we building today? ").strip()

    # Provide the agent with more context
    AIAgentFactory.get_product().run(user_prompt)
       
if __name__ == "__main__":
    run()
