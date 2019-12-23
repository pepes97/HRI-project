from agent.agent import Agent
from listener.listener import Listener
from speaker.speaker import Speaker
import stanfordnlp


# TO BUILD THE DEPENDENCIES TREE
#stanfordnlp.download('en')   # This downloads the English models for the neural pipeline
#nlp = stanfordnlp.Pipeline() # This sets up a default neural pipeline in English
#doc = nlp("Barack Obama was born in Hawaii.  He was elected president in 2008.")
#doc.sentences[0].print_dependencies()


listener = Listener()
speaker = Speaker()

bot_name = "\t\t\t\t\tAstroBot"
agent = Agent(speaker, listener, bot_name)
print(f"{bot_name}: Hi, how can I help you?")
speaker.speak("Hi, how can I help you?")

while True:
    command = listener.listen()
    command = command.strip()

    if command == "exit":
        print(f"{bot_name}: Bye bye")
        speaker.speak("Bye bye")
        break

    
    print(f"You: {command}")
        #speaker.speak(f"You said {command}")
        
        #doc = nlp(command)
        #doc.sentences[-1].print_dependencies()
        
        #TODO: process command inside the agent
    agent.process(command)

    #elif ret == Listener.UNKNOWN_VALUE:
    #    print("I didnt get that. Try to repeat")
    #    speaker.speak("I didn't get that Try to repeat")
        
    