import pyttsx3


class Speaker:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('volume', 10.0) # volume of voice
        self.engine.setProperty('rate', 125)   # voice rate that you want to set
    
    def speak(self, sentence):
        self.engine.say(sentence)
        self.engine.runAndWait()
