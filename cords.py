from pyautogui import position
from time import sleep

while True:
	try:
		print(position())
		sleep(1)
	except Exception as e:
		print("Error!\nSaved to CordsCrash.txt")
		with open("CordsCrash.txt","w") as f:
			f.write("Crash Report\n\n"+str(e))
		break