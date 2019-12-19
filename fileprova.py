import random
import datetime
import webbrowser
import pyttsx3
import wikipedia
from pygame import mixer
import speech_recognition as sr


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id) # voice set
volume = engine.getProperty('volume')   
engine.setProperty('volume', 10.0) # volume of voice
rate = engine.getProperty('rate')
engine.setProperty('rate', 125)   # voice rate that you want to set

greetings = ['hey there', 'hello', 'hi', 'hey!', 'hey']
question = ['how are you', 'how are you doing']
responses = ['Okay', "I'm fine"]
var1 = ['who made you', 'who created you']
var11 = ['i am a bot', 'i am you father, Luke']
var2 = [ ' I was made by Sveva', ' I was made by Simone', ' I was made by Marco']
var3 = ['what time is it', 'what is the time', 'time']
var4 = ['who are you', 'what is you name']
cmd2 = ['play music', 'play songs', 'play a song', 'open music player']
cmd3 = ['tell a joke', 'tell me a joke', 'say something funny', 'tell something funny']
jokes = ['Can a kangaroo jump higher than a house? Of course, a house doesn’t jump at all.', 'My dog used to chase people on a bike a lot. It got so bad, finally I had to take his bike away.', 'Doctor: Im sorry but you suffer from a terminal illness and have only 10 to live.Patient: What do you mean, 10? 10 what? Months? Weeks?!"Doctor: Nine.']
cmd6 = ['exit', 'close', 'goodbye', 'nothing']
cmd7 = ['what is your color', 'what is your colour', 'your color', 'your color?']
colrep = ['Right now its rainbow', 'Right now its transparent', 'Right now its non chromatic']
cmd9 = ['thank you']
repfr9 = ['youre welcome', 'glad i could help you']


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

def PippoResponse(audio):
    print('Pippo: '+ audio)
    engine.say(audio)
    engine.runAndWait()

def skills(command):
        
    if command in greetings:
        reply = random.choice(greetings)
        PippoResponse(reply)
        myCommand()
    elif command in question:
        reply = random.choice(responses)
        PippoResponse(reply)
        myCommand()
    elif command in var1:
        reply = random.choice(var2)
        PippoResponse(reply)
        myCommand()
    elif command in cmd9:
        reply = random.choice(repfr9)
        PippoResponse(reply)
        myCommand()
    elif command in cmd7:
        reply = random.choice(colrep)
        PippoResponse(reply)
        myCommand()
    elif command in cmd2:
        mixer.init()
        mixer.music.load("harvard.wav")
        mixer.music.play(0)
        myCommand()
    elif command in var4:
        reply = random.choice(var11)
        PippoResponse(reply)
        myCommand()
    elif command in cmd6:
        PippoResponse('Bye, see you later')
        exit()
    elif command in var3:
        print("Current date and time : ")
        reply= now.strftime("The time is %H:%M")
        PippoResponse(reply)
        myCommand()
    elif command in cmd3:
        reply = random.choice(jokes)
        PippoResponse(reply)
        myCommand()
    else:
        engine.say("please wait")
        engine.runAndWait()
        PippoResponse("please wait")
        print(wikipedia.summary(command))
        engine.say(wikipedia.summary(command))
        engine.runAndWait()
        myCommand()


if __name__ == '__main__':
    myCommand()