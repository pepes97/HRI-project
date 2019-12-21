import speech_recognition as sr

class Listener():
    OK = 0
    UNKNOWN_VALUE = 1

    def __init__(self):
        return

    def listen(self):
        r = sr.Recognizer()
        
        with sr.Microphone() as source:
            print('Say something...')
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)

            command=""
            try:
                command = r.recognize_google(audio).lower()
                ret = self.OK

            except sr.UnknownValueError:
                ret = self.UNKNOWN_VALUE
                
        return command, ret

    