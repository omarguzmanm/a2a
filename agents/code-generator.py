from typing import TypedDict
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
import os

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

model = ChatAnthropic(model='claude-3-5-sonnet-20240620', api_key=api_key)

class AgentState(TypedDict):
    steps: str
    
    
def assistant(state: AgentState) -> str:
    """
    Generate code based on the provided steps.
    """
    # Simulating code generation based on the steps
    system_message = system()
    
    message = [
        HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": f"Generate code based on the following steps: {state['steps']}"
                }
            ]
        ),
    ]
    
    response = model.invoke([system_message, *message])
    
    return response.content.strip()
    
    
def system() -> AnyMessage:
    """
    System message to set the context for the agent.
    """
    return SystemMessage(
        content="You are an expert code generator. Your task is to generate code based on the provided steps. " \
                "You do not need to provide explanations, just the code."
    )
    
def run(state: AgentState) -> str:
    """
    Run the agent with the given state.
    """
        
    assistant_message = assistant(state)
    
    return assistant_message

def main():
    """
    Main function to run the agent.
    """
    state = AgentState(steps="1. Create a function that takes two numbers and returns their sum. "
                              "2. Add error handling for non-numeric inputs.")
    
    generated_code = run(state)
    
    print("Generated Code:")
    print(generated_code)
    
if __name__ == "__main__":
    main()