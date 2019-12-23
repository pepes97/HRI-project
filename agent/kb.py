import os
from datetime import  datetime
import json

class KB:
    def __init__(self, path=None, new=False):
        if path:
            self.kb = self.load(path)
        elif new==False:
            last = os.listdir("./agent/kb")
            if len(last)==0:
                self.kb = self.new_kb()
                return    
            last.sort()
            last = last[-1]
            self.kb = self.load(last)
        else:
            self.kb = self.new_kb()

    def get_kb(self):
        return self.kb

    def new_kb(self):
        return {"systems":[]}

    def load(self, path):
        with open(f"./agent/kb/{path}") as file:
            data = json.load(file)
        return data

    def save(self, d):
        with open(f"./agent/kb/{datetime.now().strftime('%Y%m%d-%H%M%S')}_kb.json", 'x') as outfile:
            json.dump(d, outfile)
