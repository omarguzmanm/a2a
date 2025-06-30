from python_a2a import AgentNetwork, Flow
import asyncio

async def main():
    network = AgentNetwork()
    network.add("issue-analysis", "http://localhost:5000")
    network.add("code-generator", "http://localhost:5001")
    network.add("docs-generator", "http://localhost:5002")
    
    flow = Flow(agent_network=network, name="Solve issues with code generation and documentation")
    flow.ask("issue-analysis", "{issue}")
    flow.ask("code-generator", "{latest_result}")
    flow.ask("docs-generator", "{latest_result}")
    
    result = await flow.run({
        "issue": "Create a simple Python script that prints 'Hello, World!'"
    })
    
    print(result)

if __name__ == "__main__":
    asyncio.run(main())