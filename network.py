from python_a2a import AgentNetwork, A2AClient

# Create a network of agents
network = AgentNetwork(name="Issue Analysis Network")

# Add agents in different ways
network.add("analyze-issue", "http://127.0.0.1:5000")  # From URL
# network.add("medications", A2AClient("http://localhost:5002"))  # From client instance

# Discover agents from a list of URLs
# discovered_count = network.discover_agents([
#     "http://localhost:5003",
#     "http://localhost:5004",
#     "http://localhost:5005"
# ])
# print(f"Discovered {discovered_count} new agents")

# List all agents in the network
for agent_info in network.list_agents():
    print(f"Agent Info: {agent_info}")
    print(f"Agent: {agent_info['name']}")
    print(f"URL: {agent_info['url']}")
    if 'description' in agent_info:
        print(f"Description: {agent_info['description']}")
    print()

# Get a specific agent
agent = network.get_agent("analyze-issue")
response = agent.ask("I want to create a calculator in Python")
print(f"Response: {response}")