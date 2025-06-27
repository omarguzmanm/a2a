from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage
from dotenv import load_dotenv
from python_a2a import A2AServer, skill, agent, run_server, TaskStatus, TaskState
import os

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

model = ChatAnthropic(model='claude-3-5-sonnet-20240620', api_key=api_key)

@agent(
    name="Issue Analysis Agent",
    description="Analyzes issues and provides steps to resolve them",
    version="1.0.0"
)
class AnalysisAgent(A2AServer):
    # issue: str
    
    @skill(
        name="Analyze Issue",
        description="Analyze the issue and provide steps to resolve it",
        tags=["issue", "analysis", "resolution"]
    )
    def analyze_issue(self, issue: str) -> str:
        """
        Analyze the issue and provide steps to resolve it.
        """
        system_message = system()
        message = [
            HumanMessage(
                content=[
                    {
                        "type": "text",
                        "text": f"Analyze the issue: {issue} and provide the steps to resolve it."
                    }
            ]
        )]
    
        response = model.invoke([system_message, *message])
    
        return response.content.strip()
    
    def handle_task(self, task: TaskState):
        """
        Handle the task by analyzing the issue and providing steps to resolve it.
        """
        # Extract issue from task message
        message_data = task.message or {}
        content = message_data.get("content", {})
        text = content.get("text", "") if isinstance(content, dict) else ""
        
        if text:
            # Analyze the issue and get the response
            response_text = self.analyze_issue(text)
            task.artifacts = [{
                "parts": [{"type": "text", "text": response_text}]
            }]
            task.status = TaskStatus(state=TaskState.COMPLETED)
        else:
            task.status = TaskStatus(
                state=TaskState.INPUT_REQUIRED,
                message={"role": "agent", "content": {"type": "text", 
                         "text": "Please provide an issue to analyze."}}
            )
        
        return task
    
    
def system() -> AnyMessage:
    """
    System message to set the context for the agent.
    """
    return SystemMessage(
        content="You are an expert in issue analysis and resolution. "
                "Your task is to analyze the given issue and provide detailed steps to resolve it."
                "You do not need to provide solutions in code, just the steps to resolve the issue."
    )
    


if __name__ == "__main__":
    agent = AnalysisAgent()
    run_server(agent, port=5000)
