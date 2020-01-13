from agent.agent import Agent
from listener.listener import Listener
from speaker.speaker import Speaker
import stanfordnlp
import argparse

parser = argparse.ArgumentParser(description='An interactive bot to talk about stars and planets')
parser.add_argument('--dep_tree', default=False, type=bool, help='print dependencies tree of every heard sentence (default: False)')
parser.add_argument("--kb_file", help="file containing the knowledge-base (dafault: the last updated file in the kb directory)")

args = parser.parse_args()

# TO BUILD THE DEPENDENCIES TREE
if args.dep_tree:
    stanfordnlp.download('en')   # This downloads the English models for the neural pipeline
    print('Building pipeline...')
    nlp = stanfordnlp.Pipeline() # This sets up a default neural pipeline in English

listener = Listener()
speaker = Speaker()

bot_name = "\t\t\t\t\tAstroBot"
agent = Agent(speaker, listener, bot_name, args.kb_file)
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
    if args.dep_tree:
        
        doc = nlp(command)
        print('\n')
        print('TOKENS OF COMMAND \n')
        print(*[f'text: {word.text+" "}\tlemma: {word.lemma}\tupos: {word.upos}\txpos: {word.xpos}' 
                for sent in doc.sentences 
                    for word in sent.words], sep='\n') 
        print('---------------------------------------------')
        print('DEPENDENCY PARSE OF COMMAND \n')
        doc.sentences[-1].print_dependencies()
               
    agent.process(command)
