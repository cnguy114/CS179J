from gpiozero import Button
from gpiozero import LED
from time import sleep
import camCap
#this checks a a gpio from the arduino. If the pin goes high, there is an object on the staging area

photoRes = Button(26)
sig0 = LED(20)
sig1 = LED(21)
ready = LED(16)
state = 3
#check for arduino signal
ready.on()
def sendMsg(c):
	if c == 3:
		sig0.off()
		sig1.off()
	elif c == 0:
		sig0.on()
		sig1.off()
	elif c == 1:
		sig0.off()
		sig1.on()
	elif c == 2:
		sig0.on()
		sig1.on()
	else:
		print("ERROR: Invalid Classification")
	sleep(3)

def imgCap():
    return camCap.takePic()

def changeState():
    if photoRes.is_pressed:
        return imgCap()
    else:
        return 3

while True:
    print ("Changing State")
    state = changeState()
    
    print ("state: " + str(state))
    sendMsg(state)
