from typing import TypedDict
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from python_a2a import A2AServer, skill, agent, run_server, TaskStatus, TaskState
import os

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

model = ChatAnthropic(model='claude-3-5-sonnet-20240620', api_key=api_key)

@agent(
    name="Code Generation Agent",
    description="Generates code based on provided steps",
    version="1.0.0"
)
class CoderAgent(A2AServer):
    # steps: str
    
    @skill(
        name="Generate Code",
        description="Generate code based on the provided steps",
        tags=["code", "generation", "steps"]
    )
    def generate_code(self, steps: str) -> str:
        """
        Generate code based on the provided steps.
        """
        system_message = system()
        
        message = [
            HumanMessage(
                content=[
                    {
                        "type": "text",
                        "text": f"Generate code based on the following steps: {steps}"
                    }
                ]
            ),
        ]
        
        response = model.invoke([system_message, *message])
        
        return response.content.strip()
    
    def handle_task(self, task: TaskState):
        """
        Handle the task by generating code based on the provided steps.
        """
        # Extract steps from task message
        message_data = task.message or {}
        content = message_data.get("content", {})
        text = content.get("text", "") if isinstance(content, dict) else ""
        
        if text:
            # Generate code and get the response
            response_text = self.generate_code(text)
            task.artifacts = [{
                "parts": [{"type": "text", "text": response_text}]
            }]
            task.status = TaskStatus(state=TaskState.COMPLETED)
        else:
            task.status = TaskStatus(
                state=TaskState.INPUT_REQUIRED,
                message={"role": "agent", "content": {"type": "text", "text": "Please provide the steps to generate code."}}
            )
            
        return task
    

def system() -> AnyMessage:
    """
    System message to set the context for the agent.
    """
    return SystemMessage(
        content="You are an expert code generator. Your task is to generate code based on the provided steps. " \
                "You do not need to provide explanations, just the code."
    )
    

if __name__ == "__main__":
    agent = CoderAgent()
    run_server(agent, port=5001)