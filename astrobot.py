
import nltk
from nltk.corpus.reader import WordListCorpusReader
import random
import datetime
import webbrowser
import pyttsx3
import wikipedia
from pygame import mixer
import speech_recognition as sr

reader = WordListCorpusReader('.', ['earth.txt', 'mars.txt'])

print(reader.words())
print(reader.fileids())


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id) # voice set
volume = engine.getProperty('volume')   
engine.setProperty('volume', 10.0) # volume of voice
rate = engine.getProperty('rate')
engine.setProperty('rate', 125)   # voice rate that you want to set

#first command to say about which argument you are teaching the bot
def myCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio).lower()
            print('You said: ' + command + '\n')
            skills(command)
        #loop back to continue to listen for commands if unrecognizable speech is received
        except sr.UnknownValueError:
            print('Pippo : ....')
            engine.say('I didnt get that. Rerun the code')
            engine.runAndWait()
            command = myCommand()

#teaching new stuff
def teach():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Ready to obtain info')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio).lower()
            print('You said: ' + command + '\n')
            return command
        #loop back to continue to listen for commands if unrecognizable speech is received
        except sr.UnknownValueError:
            print('Pippo : ....')
            engine.say('I didnt get that. Rerun the code')
            engine.runAndWait()
            command = myCommand()

def PippoResponse(audio):
    print('Pippo: '+ audio)
    engine.say(audio)
    engine.runAndWait()

def skills(command):   
    if command=="1":
        s=""
        f = open("mars.txt", "a")
        while s!="stop":
            s=teach()
            if(s!="stop"):
                f.write(s+'\n')
        print("stop")
        f.close()

    else:
        engine.say("please wait")
        engine.runAndWait()
        PippoResponse("please wait")
        engine.runAndWait()
        myCommand()


if __name__ == '__main__':
    myCommand()

