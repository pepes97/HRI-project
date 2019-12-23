import re
import sys
from agent.kb import KB

class Agent:
    templates = {
        "save":["save", "save knowledge", "save your knowledge"],
        #save

        "ask_all_about_system":["what do you know about (?P<system_name>[a-z]+) system", "talk me about (?P<system_name>[a-z]+) system", "tell me about (?P<system_name>[a-z]+) system", "talk to me about (?P<system_name>[a-z]+) system"],
        # talk me about solar system
        
        "ask_all_about_planet":["what do you know about (?P<planet_name>[a-z]+)", "talk me about (?P<planet_name>[a-z]+)", "tell me about (?P<planet_name>[a-z]+)", "talk to me about (?P<planet_name>[a-z]+)"],
        # tell me about jupiter

        "ask_all":["what do you know", "tell me all", "tell me all you know", "total report"],
        # what do you know
        
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
        
        "ask_star":["tell me star of (?P<system_name>[a-z]+) system", "star of (?P<system_name>[a-z]+) system"],
        # star of solar system
        
        "tell_planet":["(?P<planet_name>[a-z]+) is a planet of (?P<system_name>[a-z]+) system"],
        # mars is a planet of solar system
        
        "tell_star":["(?P<star_name>[a-z]+) is the star of (?P<system_name>[a-z]+) system"],
        # sun is the star of solar system
        
        "tell_radius":["the radius of (?P<planet_name>[a-z]+) is (?P<radius>[0-9-z]+) [km|kilometres|kilometres]", "(?P<planet_name>[a-z]+) has radius (?P<radius>[0-9-z]+) [km|kilometres|kilometres]", "(?P<planet_name>[a-z]+) has a radius of (?P<radius>[0-9-z]+) [km|kilometres|kilometres]"],
        # the radius of jupiter is 10 km

        "tell_mass":["the mass of (?P<planet_name>[a-z]+) is (?P<mass>[0-9-z]+) [kg|kilograms]", "(?P<planet_name>[a-z]+) has mass (?P<mass>[0-9-z]+) [kg|kilograms]", "(?P<planet_name>[a-z]+) has a mass of (?P<mass>[0-9-z]+) [kg|kilograms]"],
        # jupiter has mass of 10 kilograms

        "tell_temperature":["the temperature of (?P<planet_name>[a-z]+) is (?P<temperature>[0-9-z]+) [degrees]", "(?P<planet_name>[a-z]+) has temperature (?P<temperature>[0-9-z]+) [degrees]"],
        # jupiter has mass of 10 kilograms

        "tell_orbit_time":["the orbital period of (?P<planet_name>[a-z]+) is (?P<orbit_time>[0-9]+ [year|month|years|months])",
                           "the orbital period of (?P<planet_name>[a-z]+) is of (?P<orbit_time>[0-9]+ [year|month|years|months])",
                           "orbital period of (?P<planet_name>[a-z]+) is (?P<orbit_time>[0-9]+ [year|month|years|months])",
                           "orbital period of (?P<planet_name>[a-z]+) is of (?P<orbit_time>[0-9]+ [year|month|years|months])", 
                           "(?P<planet_name>[a-z]+) has orbital period of (?P<orbit_time>[0-9]+ [year|month|years|months])",
                           "(?P<planet_name>[a-z]+) has a orbital period of (?P<orbit_time>[0-9]+ [year|month|years|months])"],
        # the orbital period of jupiter is 10 years
        
        "ask_radius":["what is the radius of (?P<planet_name>[a-z]+)", "radius of (?P<planet_name>[a-z]+)"],
        # radius of jupiter
        
        "ask_mass":["what is the mass of (?P<planet_name>[a-z]+)", "mass of (?P<planet_name>[a-z]+)"],
        # mass of jupiter

        "ask_temperature":["what is the temperature of (?P<planet_name>[a-z]+)", "temperature of (?P<planet_name>[a-z]+)"],
        # mass of jupiter

        "ask_orbit_time":["what is the orbital period of (?P<planet_name>[a-z]+)", "orbital period of (?P<planet_name>[a-z]+)",
                        "the orbital period of (?P<planet_name>[a-z]+)"],
        # orbital period of jupiter 

        "ask_largest_planet":["what is the largest planet of (?P<system_name>[a-z]+)", "largest planet of (?P<system_name>[a-z]+)" ],
        # largest planet of solar system
        
        "ask_smallest_planet":["what is the smallest planet of (?P<system_name>[a-z]+)", "smallest planet of (?P<system_name>[a-z]+)" ],
        # smallest planet of solar system
        
        "ask_hottest_planet":["what is the hottest planet of (?P<system_name>[a-z]+)", "hottest planet of (?P<system_name>[a-z]+)" ],
        # hottest planet of solar system
        
        "ask_coldest_planet":["what is the coldest planet of (?P<system_name>[a-z]+)", "coldest planet of (?P<system_name>[a-z]+)" ],
        # smallest planet of solar system
        
        "ask_fastest_planet":["what is the fastest planet of (?P<system_name>[a-z]+)", "fastest planet of (?P<system_name>[a-z]+)" ],
        # fastest planet of solar system
        
        "ask_slowest_planet":["what is the slowest planet of (?P<system_name>[a-z]+)", "slowest planet of (?P<system_name>[a-z]+)" ]
        # slowest planet of solar system
        }

    def __init__(self, speaker, listener, name, kb_file):
        self.name = name
        self.speaker = speaker
        self.listener = listener
        self.kb_manager = KB(kb_file)
        self.kb = self.kb_manager.get_kb()

    def check_match(self, command):
        for key in Agent.templates:
            for i, pattern in enumerate(Agent.templates[key]):

                match = re.search(pattern, command)
                if match:
                    return key, i
        return None, 0

    def act(self, key, pattern, command):
        if "tell" in key:
            approved = self.wait_for_approval()
            if not approved:
                self.say("I don't learn this")
                return
        if key == "save":
            self.kb_manager.save(self.kb)
            self.say_ok()

        elif key=="tell_system":
            m = re.match(pattern, command)
            name = m.group("name")
            self.kb["systems"].append({"system":name,"star":"","planets":[]})
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
            
        elif key=="tell_star":
            m = re.match(pattern, command)
            star_name = m.group("star_name")            
            system_name = m.group("system_name")
            for i, system in enumerate(self.kb["systems"]):
                if system["system"]==system_name:
                    self.kb["systems"][i]["star"] = star_name 
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
        
        elif key == "ask_star":
            m = re.match(pattern, command)
            system_name = m.group("system_name")

            for i, system in enumerate(self.kb["systems"]):
                if system["system"]==system_name:
                    if(system["star"]!=""):
                        self.say(f"I know the star of {system_name} system")
                        self.say(system['star'])
                    else:
                        self.say(f"I don't know the star of {system_name} system")
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
        
        elif key == "tell_radius":
            m = re.match(pattern, command)
            planet = m.group("planet_name")
            radius = m.group("radius")
            for i, system in enumerate(self.kb["systems"]):
                for j, p in enumerate(self.kb["systems"][i]["planets"]):
                    if p["planet"]==planet:
                        p["radius"]=radius
                        self.say_ok()
                        return
            self.say(f"Sorry i don't know {planet} planet")

        elif key == "ask_radius":
            m = re.match(pattern, command)
            planet = m.group("planet_name")
            for i, system in enumerate(self.kb["systems"]):
                for j, p in enumerate(self.kb["systems"][i]["planets"]):
                    if p["planet"]==planet:
                        if p["radius"]:
                            self.say(f"The radius of {planet} is {p['radius']} kilometers")
                            return
                        else:
                            self.say(f"Sorry, I don't know the radius of {planet}")
                            return
            self.say(f"Sorry i don't know {planet} planet")

        elif key == "tell_mass":
            m = re.match(pattern, command)
            planet = m.group("planet_name")
            mass = m.group("mass")
            for i, system in enumerate(self.kb["systems"]):
                for j, p in enumerate(self.kb["systems"][i]["planets"]):
                    if p["planet"]==planet:
                        p["mass"]=mass
                        self.say_ok()
                        return
            self.say(f"Sorry i don't know {planet} planet")

        elif key == "ask_mass":
            m = re.match(pattern, command)
            planet = m.group("planet_name")
            for i, system in enumerate(self.kb["systems"]):
                for j, p in enumerate(self.kb["systems"][i]["planets"]):
                    if p["planet"]==planet:
                        if p["mass"]:
                            self.say(f"The mass of {planet} is {p['mass']} kilograms")
                            return
                        else:
                            self.say(f"Sorry, I don't know the mass of {planet}")
                            return
            self.say(f"Sorry i don't know {planet} planet")  

        elif key == "tell_temperature":
            m = re.match(pattern, command)
            planet = m.group("planet_name")
            temperature = m.group("temperature")
            for i, system in enumerate(self.kb["systems"]):
                for j, p in enumerate(self.kb["systems"][i]["planets"]):
                    if p["planet"]==planet:
                        p["temperature"]=temperature
                        self.say_ok()
                        return
            self.say(f"Sorry i don't know {planet} planet")

        elif key == "ask_temperature":
            m = re.match(pattern, command)
            planet = m.group("planet_name")
            for i, system in enumerate(self.kb["systems"]):
                for j, p in enumerate(self.kb["systems"][i]["planets"]):
                    if p["planet"]==planet:
                        if p["temperature"]:
                            self.say(f"The temperature of {planet} is {p['temperature']} degrees")
                            return
                        else:
                            self.say(f"Sorry, I don't know the temperature of {planet}")
                            return
            self.say(f"Sorry i don't know {planet} planet")       

        elif key == "tell_orbit_time":
            m = re.match(pattern, command)
            planet = m.group("planet_name")
            orbit_time = m.group("orbit_time")
            for i, system in enumerate(self.kb["systems"]):
                for j, p in enumerate(self.kb["systems"][i]["planets"]):
                    if p["planet"]==planet:
                        p["orbit_time"]=orbit_time
                        self.say_ok()
                        return
            self.say(f"Sorry i don't know {planet} planet")
        
        elif key == "ask_orbit_time":
            m = re.match(pattern, command)
            planet = m.group("planet_name")
            for i, system in enumerate(self.kb["systems"]):
                for j, p in enumerate(self.kb["systems"][i]["planets"]):
                    if p["planet"]==planet:
                        if p["orbit_time"]:
                            self.say(f"The orbit time of {planet} is {p['orbit_time'][:-2]} {'months' if p['orbit_time'][-1]=='m' else 'years'}")
                            return
                        else:
                            self.say(f"Sorry, I don't know the orbit time of {planet}")
                            return
            self.say(f"Sorry i don't know {planet} planet")  

        elif key=="ask_all":
            n = len(self.kb["systems"])
            self.say(f"I know {n} different systems")
            for i, system in enumerate(self.kb["systems"]):
                self.say(f"{system['system']} system")

            for i, system in enumerate(self.kb["systems"]):
                self.say(f"I know {len(system['planets'])} planets of {system['system']} system")
                if len(system['planets'])>0:
                    self.say(f"The planets that i know in {system['system']} system are")
                for p in system["planets"]:
                    self.say(p['planet'])
                for p in system["planets"]:
                    if p["radius"]:
                        self.say(f"The radius of {p['planet']} is {p['radius']} kilometers")
                    if p["mass"]:
                        self.say(f"The mass of {p['planet']} is {p['mass']} kilograms")
                    if p["orbit_time"]:
                        self.say(f"The orbit time of {p['planet']} is {p['orbit_time'][:-2]} {'months' if p['orbit_time'][-1]=='m' else 'years'}")
        elif key == "ask_all_about_system":
            m = re.match(pattern, command)
            system_name = m.group("system_name")

            for i, system in enumerate(self.kb["systems"]):
                if system["system"]==system_name:
                    self.say(f"I know {len(system['planets'])} planets of {system['system']} system")
                    if len(system['planets'])>0:
                        self.say(f"The planets that i know in {system['system']} system are")
                    for p in system["planets"]:
                        self.say(p['planet'])
                    for p in system["planets"]:
                        if p["radius"]:
                            self.say(f"The radius of {p['planet']} is {p['radius']} kilometers")
                        if p["mass"]:
                            self.say(f"The mass of {p['planet']} is {p['mass']} kilograms")
                        if p["orbit_time"]:
                            self.say(f"The orbit time of {p['planet']} is {p['orbit_time'][:-2]} {'months' if p['orbit_time'][-1]=='m' else 'years'}")                    
                    return
            self.say(f"Sorry, I don't know {system_name} system")

        elif key == "ask_all_about_planet":
            m = re.match(pattern, command)
            planet = m.group("planet_name")
            for i, system in enumerate(self.kb["systems"]):
                for j, p in enumerate(self.kb["systems"][i]["planets"]):
                    if p["planet"]==planet:
                        self.say(f"{planet} is a planet of {system['system']} system")
                        if p["radius"]:
                            self.say(f"The radius of {planet} is {p['radius']} kilometers")
                        if p["mass"]:
                            self.say(f"The mass of {planet} is {p['mass']} kilograms")
                        if p["orbit_time"]:
                            self.say(f"The orbit time of {planet} is {p['orbit_time'][:-2]} {'months' if p['orbit_time'][-1]=='m' else 'years'}")
                        return
            self.say(f"Sorry i don't know {planet} planet")
            
        elif key == "ask_largest_planet":
            m = re.match(pattern, command)
            system_name = m.group("system_name")
            for i, system in enumerate(self.kb["systems"]):
                if system["system"]==system_name:
                    largest_planet_name = self.largest_planet(system,0)
                    self.say(f"{largest_planet_name} is the largest planet of {system_name} system")
                return
            self.say(f"Sorry i don't know {system_name} system")
            
        elif key == "ask_smallest_planet":
            m = re.match(pattern, command)
            system_name = m.group("system_name")
            for i, system in enumerate(self.kb["systems"]):
                if system["system"]==system_name:
                    smallest_planet_name = self.smallest_planet(system,int(sys.float_info.max))
                    self.say(f"{smallest_planet_name} is the smallest planet of {system_name} system")
                return
            self.say(f"Sorry i don't know {planet} planet")
            
        elif key == "ask_hottest_planet":
            m = re.match(pattern, command)
            system_name = m.group("system_name")
            for i, system in enumerate(self.kb["systems"]):
                if system["system"]==system_name:
                    hottest_planet_name = self.hottest_planet(system,int(sys.float_info.max))
                    self.say(f"{hottest_planet_name} is the hottest planet of {system_name} system")
                return
            self.say(f"Sorry i don't know {planet} planet")
            
        elif key == "ask_coldest_planet":
            m = re.match(pattern, command)
            system_name = m.group("system_name")
            for i, system in enumerate(self.kb["systems"]):
                if system["system"]==system_name:
                    coldest_planet_name = self.coldest_planet(system,int(sys.float_info.max))
                    self.say(f"{coldest_planet_name} is the coldest planet of {system_name} system")
                return
            self.say(f"Sorry i don't know {planet} planet")
        
        elif key == "ask_fastest_planet":
            m = re.match(pattern, command)
            system_name = m.group("system_name")
            for i, system in enumerate(self.kb["systems"]):
                if system["system"]==system_name:
                    fastest_planet_name = self.fastest_planet(system,"y",int(sys.float_info.max))
                    self.say(f"{fastest_planet_name} is the fastest planet of {system_name} system")
                return
            self.say(f"Sorry i don't know {planet} planet")
        
        elif key == "ask_slowest_planet":
            m = re.match(pattern, command)
            system_name = m.group("system_name")
            for i, system in enumerate(self.kb["systems"]):
                if system["system"]==system_name:
                    slowest_planet_name = self.slowest_planet(system,"",0)
                    self.say(f"{slowest_planet_name} is the slowest planet of {system_name} system")
                return
            self.say(f"Sorry i don't know {planet} planet")
            
    def process(self, command):
        key, i = self.check_match(command)
        if key:
            self.act(key, Agent.templates[key][i], command)

        else:
            self.say_not_understood()

        #print(self.kb)
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
    
    def largest_planet(self,system,max):
        max_planet=""
        for p in system["planets"]:
            if (p["radius"]!=None):
                if (int(p["radius"])>max):
                    max=int(p["radius"])
                    max_planet = p['planet'] 
        if (max_planet == ""):
            self.say_not_known()
        return max_planet
    
    def smallest_planet(self,system,min):
        min_planet=""
        for p in system["planets"]:
            if (p["radius"]!=None):
                if (int(p["radius"])<min):
                    min=int(p["radius"])
                    min_planet = p['planet'] 
        if (min_planet == ""):
            self.say_not_known()
        return min_planet
    
    def hottest_planet(self,system,hot_max):
        hot_planet=""
        for p in system["planets"]:
            if (p["temperature"]!=None):
                if (int(p["temperature"])>hot_max):
                    hot_max=int(p["temperature"])
                    hot_planet = p['planet'] 
        if (hot_planet == ""):
            self.say_not_known()            
        return hot_planet
    
    def coldest_planet(self,system,cold_min):
        cold_planet=""
        for p in system["planets"]:
            if (p["temperature"]!=None):
                if (int(p["temperature"])<cold_min):
                    cold_min=int(p["temperature"])
                    cold_planet = p['planet'] 
        if (cold_planet == ""):
            self.say_not_known()
        return cold_planet
    
    def fastest_planet(self,system,time_max,fast_min):
        fast_planet=""
        for p in system["planets"]:
            if (p["orbit_time"]!=None):
                if (p["orbit_time"].split()[1]<time_max):
                    time_max=p["orbit_time"].split()[1]
                    fast_min = int(p["orbit_time"].split()[0])
                    fast_planet = p['planet'] 
                elif (p["orbit_time"].split()[1]==time_max):
                    if(int(p["orbit_time"].split()[0])<fast_min):
                        fast_min = int(p["orbit_time"].split()[0])
                        fast_planet = p['planet'] 
        if (fast_planet == ""):
            self.say_not_known()            
        return fast_planet
    
    def slowest_planet(self,system,time_min,slow_max):
        slow_planet=""
        for p in system["planets"]:
            if (p["orbit_time"]!=None):
                if (p["orbit_time"].split()[1]>time_min):
                    time_min=p["orbit_time"].split()[1]
                    slow_max = int(p["orbit_time"].split()[0])
                    slow_planet = p['planet'] 
                elif (p["orbit_time"].split()[1]==time_min):
                    if(int(p["orbit_time"].split()[0])>slow_max):
                        slow_max = int(p["orbit_time"].split()[0])
                        slow_planet = p['planet'] 
        if (slow_planet == ""):
            self.say_not_known()            
        return slow_planet
    
    def wait_for_approval(self):
        self.say("Are you sure?")
        command = self.listener.listen()
        print(f"You: {command}")

        while command!= "yes" and command!="no":
            command = self.listener.listen()
            print(f"You: {command}")
        if command=="yes":
            return True
        else:
            return False