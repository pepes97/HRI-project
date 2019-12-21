from agent.agent import Agent
from listener.listener import Listener
from speaker.speaker import Speaker

listener = Listener()
speaker = Speaker()
while True:
    command, ret = listener.listen()
    
    if command == "exit":
        speaker.speak("Bye bye")
        break

    if ret == Listener.OK:
        print(f"You said: {command}")
        speaker.speak(f"You said {command}")

    elif ret == Listener.UNKNOWN_VALUE:
        print("I didnt get that. Try to repeat")
        speaker.speak("I didnt get that. Try to repeat")
        
    else:
        print("Unknown return value from listener")