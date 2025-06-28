from python_a2a import AgentNetwork, Flow
import asyncio

async def main():
    network = AgentNetwork()
    network.add("issue-analysis", "http://localhost:5001")
    network.add("code-generator", "http://localhost:5002")
    network.add("docs-generator", "http://localhost:5003")
    
    flow = Flow(agent_network=network, name="Solve issues with code generation and documentation")
    flow.ask("issue-analysis", "{issue}")
    
    parallel_results = (flow.parallel()
        .ask("code-generator", "{latest_result}")
        .branch()
        .ask("docs-generator", "{latest_result}")
        .end_parallel(max_concurrency=2))
    
    flow.execute_function(
        lambda results, context: f"Code: {results['1']}\nDocs : {results['2']}",
        parallel_results
    )
    
    # Execute the workflow
    result = await flow.run({
        "issue": "Create a simple Python script that prints 'Hello, World!'"
    })
    
    print(result)

if __name__ == "__main__":
    asyncio.run(main())