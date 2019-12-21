import pyttsx3


class Speaker:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[2].id) # voice set
        self.volume = self.engine.getProperty('volume')   
        self.engine.setProperty('volume', 10.0) # volume of voice
        self.rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', 125)   # voice rate that you want to set

        return

    def speak(self, sentence):
        self.engine.say(sentence)
        self.engine.runAndWait()
