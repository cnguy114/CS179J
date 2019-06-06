from gpiozero import LED
from gpiozero import Button

sig0 = LED(20)
sig1 = LED(21)

def sendMsg(state):
    if state == 0:
        sig0.off()
        sig1.off()

    elif state == 1:
        sig0.on()
        sig1.off()

    elif state == 2:
        sig0.off()
        sig1.on()

    elif state == 3:
        sig0.on()
        sig1.on()
    
    else:
        print("Error:INVALID CLASSIFICATION")
