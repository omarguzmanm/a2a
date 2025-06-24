from typing import TypedDict
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

model = ChatAnthropic(model='claude-3-5-sonnet-20240620', api_key=api_key)

class AgentState(TypedDict):
    issue: str

def assistant(state: AgentState) -> str:
    """
    Analyze the issue and provide the steps to resolve it.
    """
    system_message = system()

    message = [
        HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": f"Analyze the issue: {state['issue']} and provide the steps to resolve it."
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
        content="You are an expert in issue analysis and resolution. "
                "Your task is to analyze the given issue and provide detailed steps to resolve it."
                "You do not need to provide solutions in code, just the steps to resolve the issue."
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

    state = AgentState(issue="The application crashes when I try to open it.")
    
    result = run(state)
    
    print("Analysis Result:")
    print(result)
    

if __name__ == "__main__":
    main()