from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage
from dotenv import load_dotenv
from python_a2a import A2AServer, skill, agent, run_server, TaskStatus, TaskState
import os

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

model = ChatAnthropic(model='claude-3-5-sonnet-20240620', api_key=api_key)

@agent(
    name="Documentation Generator Agent",
    description="Generates documentation based on provided source code",
    version="1.0.0"
)
class DocsAgent(A2AServer):
    
    @skill(
        name="Generate Documentation",
        description="Generate documentation based on thesource code",
        tags=["documentation", "generation", "issue analysis"]
    )
    def generate_documentation(self, code: str) -> str:
        """
        Generate documentation based on the provided issue analysis and source code.
        """
        system_message = system()
        
        message = [
            HumanMessage(
                content=[
                    {
                        "type": "text",
                        "text": f"Generate documentation based on the following source code: {code}"
                    }
                ]
            ),
        ]
        
        response = model.invoke([system_message, *message])
        
        return response.content.strip()
    
    def handle_task(self, task: TaskState):
        """
        Handle the task by generating documentation based on the provided source code.
        """
        # Extract issue from task message
        message_data = task.message or {}
        print(f"Message data: {message_data}")
        content = message_data.get("content", {})
        text = content.get("text", "") if isinstance(content, dict) else ""
        
        if text:
            # Generate documentation and get the response
            response_text = self.generate_documentation(text)
            task.artifacts = [{
                "parts": [{"type": "text", "text": response_text}]
            }]
            task.status = TaskStatus(state=TaskState.COMPLETED)
        else:
            task.status = TaskStatus(
                state=TaskState.INPUT_REQUIRED,
                message={"role": "agent", "content": {"type": "text", "text": "Please provide source code to generate documentation."}}
            )
        
        return task
    
    
def system() -> AnyMessage:
    """
    System message to set the context for the agent.
    """
    return SystemMessage(
        content="You are a documentation generation agent. Your task is to generate documentation based on the provided source code. "
                "You will receive source code as input, and you should generate clear and concise documentation for it. "
    )
    

if __name__ == "__main__":
    agent = DocsAgent()
    run_server(agent, port=5002)
