from agent import Agent
import re

pattern = "[a-z]+ is a system"
string = "solar is a system"

match = re.search(pattern, string)
print(match)

agent = Agent(None)
agent.check_match(string)