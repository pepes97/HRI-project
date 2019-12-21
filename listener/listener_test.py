from listener import Listener

lis = Listener()

while True:
    command, ret = lis.listen()
    if ret == Listener.OK:
        print(f"You said: {command}")

    elif ret == Listener.UNKNOWN_VALUE:
        print("I didnt get that. Try to repeat")
        
    else:
        print("Unknown return value from listener")