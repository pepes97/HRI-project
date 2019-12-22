import re

class Agent:
    templates = {
        "ask_system":["what systems do you know", "talk me about systems you know"],
        # what systems do you know
        
        "tell_system":["(?P<name>[a-z]+) is a system"],
        # solar is a system
        
        "ask_number_system":["how many systems do you know", "how many systems you know"],
        # how many systems do you know

        "ask_number_planet":["how many planets has (?P<system_name>[a-z]+) system", "number of planets of (?P<system_name>[a-z]+) system", "tell me the number of planets of (?P<system_name>[a-z]+) system"],
        # number of planets of solar system
        
        "ask_planet":["tell me planets of (?P<system_name>[a-z]+) system", "planets of (?P<system_name>[a-z]+) system"],
        # planets of solar system
        
        "tell_planet":["(?P<planet_name>[a-z]+) is a planet of (?P<system_name>[a-z]+) system"],
        # mars is a planet of solar system
        
        "ask_radius":[],
        "ask_mass":[],
        "ask_orbit_time":[],
        "ask_temperature":[],
        "tell_radius":["the radius of [a-z]+ is [0-9]+ km", "[a-z]+ has radius [0-9]+ km", "[a-z]+ has a radius of [0-9]+ km"],
        "tell_mass":["the mass of [a-z]+ is [0-9]+ kg", "[a-z]+ has mass [0-9]+ kg", "[a-z]+ has a mass of [0-9]+ kg"],
        "tell_orbit_time":["the orbit time of [a-z]+ is [0-9]+ [year|month|years|months]","The orbit time of [a-z]+ is of [0-9]+ [year|month|years|months]", "[a-z]+ has orbit time [0-9]+ [year|month|years|months]", "[a-z]+ has a orbit time of [0-9]+ [year|month|years|months]"],
        "tell_temperature":["the temperature of [a-z]+ is [0-9]+ [degrees [Celsius]?]?", "[a-z]+ has temperature [0-9]+ [degrees [Celsius]?]?", "[a-z]+ has a temperature of [0-9]+ [degrees [Celsius]?]?"]
        }

    def __init__(self, speaker, name):
        self.name = name
        self.speaker = speaker
        self.kb = {"systems":[]}

    def check_match(self, command):
        for key in Agent.templates:
            for i, pattern in enumerate(Agent.templates[key]):

                match = re.search(pattern, command)
                if match:
                    return key, i
        return None, 0

    def act(self, key, pattern, command):
        if key=="tell_system":
            m = re.match(pattern, command)
            name = m.group("name")
            self.kb["systems"].append({"system":name,"planets":[]})
            self.say_ok()

        elif key=="ask_number_system":
            n = len(self.kb["systems"])
            self.say(f"I know {n} different systems")

        elif key=="tell_planet":
            m = re.match(pattern, command)
            planet_name = m.group("planet_name")            
            system_name = m.group("system_name")
            for i, system in enumerate(self.kb["systems"]):
                if system["system"]==system_name:
                    self.kb["systems"][i]["planets"].append({"planet":planet_name,"radius":None,"mass":None,"orbit_time":None,"temperature":None})           
                    self.say_ok()
                    return
            self.say(f"Sorry, I don't know {system_name} system")

        elif key == "ask_system":
            n = len(self.kb["systems"])
            self.say(f"I know {n} different systems")
            for i, system in enumerate(self.kb["systems"]):
                self.say(f"{system['system']} system")

        elif key == "ask_planet":
            m = re.match(pattern, command)
            system_name = m.group("system_name")

            for i, system in enumerate(self.kb["systems"]):
                if system["system"]==system_name:
                    self.say(f"I know {len(system['planets'])} planets of {system_name} system")
                    if len(system['planets'])>0:
                        self.say(f"The planets that i know are")
                    for p in system["planets"]:
                        self.say(p['planet'])
                    return
            self.say(f"Sorry, I don't know {system_name} system")
        
        elif key == "ask_number_planet":
            m = re.match(pattern, command)
            system_name = m.group("system_name")

            for i, system in enumerate(self.kb["systems"]):
                if system["system"]==system_name:
                    self.say(f"I know {len(system['planets'])} planets of {system_name} system")
                    return
            self.say(f"Sorry, I don't know {system_name} system")

    def process(self, command):
        key, i = self.check_match(command)
        if key:
            self.act(key, Agent.templates[key][i], command)

        else:
            self.say_not_understood()

        print(self.kb)
    def say_ok(self):
        print(f"{self.name}: OK")
        self.speaker.speak("ok")
    
    def say_not_known(self):
        print(f"{self.name}: I don't have this information")
        self.speaker.speak("i do not have this information")

    def say_not_understood(self):
        print(f"{self.name}: probably I didn't understand what you said")
        self.speaker.speak("probably I didn't understand what you said")

    def say(self, sentence):
        print(f"{self.name}: {sentence}")
        self.speaker.speak(sentence)
    
        
        