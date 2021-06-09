#import pyautogui
import sys
import time
import python_imagesearch.imagesearch as imgsearch
from pyclick import HumanClicker
from pynput import keyboard
import json
from timer import Timer
import ctypes

#Scan config file
with open("config.json",encoding ="UTF-8") as jsonFile:
	config = json.load(jsonFile)

#pyautogui.FAILSAFE = False

user32 = ctypes.windll.user32
c_screensize = int(user32.GetSystemMetrics(0)/2), int(user32.GetSystemMetrics(1)/2)

controller = keyboard.Controller()

exec_stop = False

def run():
	global config
	global screensize
	global controller

	tm = Timer() # Mine timer
	#c_tm = Timer() # Crash timer

	approve = False
	robot = True
	cap_pressed = False
	hc = HumanClicker()
	# While there's no 'execution stop' command passed
	print("Watcher started")
	while exec_stop is False:
		try:
			if tm.status():
				if tm.get_time()>config["timer_e"]:
					print("Timer>config_time\nRestarting page")
					if tm.status():
						tm.stop()
					hc.move(c_screensize,1)
					hc.click()
					controller.press(keyboard.Key.f5)
					controller.release(keyboard.Key.f5)


			# Mine button
			if imgsearch.imagesearch("img/mine.png")[0] != -1:
				if config["mode"] == "auto":
					#print("mine")
					pos = imgsearch.imagesearch("img/mine.png")
					if pos[0]<0 or pos[1]<0:
						continue
					hc.move((pos[0]-config["oth_mons"]+config["calibrate"],pos[1]+config["calibrate"]), 1)
					hc.click()
					if not tm.status():
						tm.stop()
						tm.start()
				elif config["mode"] == "cords":
					hc.move(config["cords"]["mine"], 1)
					hc.click()
					if not tm.status():
						tm.stop()
						tm.start()

			#time.sleep(1)
			# Claim TLM button
			elif imgsearch.imagesearch("img/claim.png")[0] != -1 and imgsearch.imagesearch("img/clime_false.png")[0] == -1:
				if config["mode"] == "auto":
					#print("claim")
					pos =  imgsearch.imagesearch("img/claim.png")
					if pos[0]<0 or pos[1]<0:
						continue
					hc.move((pos[0]-config["oth_mons"]+config["calibrate"],pos[1]+config["calibrate"]), 1)
					hc.click()
				elif config["mode"] == "cords":
					hc.move(config["cords"]["claim"], 1)
					hc.click()

			# Authorize transaction button
			elif imgsearch.imagesearch("img/captcha_solved.png")[0] != -1 and cap_pressed!=True:
				if config["mode"] == "auto":
					#print("cap")
					pos = imgsearch.imagesearch("img/captcha_solved.png")
					if pos[0]<0 or pos[1]<0:
						continue
					hc.move((pos[0]-config["oth_mons"]+config["calibrate"],pos[1]+config["calibrate"]), 1)
					hc.click()
				elif config["mode"] == "cords":
					hc.move(config["cords"]["captcha"], 1)
					hc.click()

			elif imgsearch.imagesearch("img/robot.png")[0] != -1 and robot:
				if config["mode"] == "auto":
					#print("robot")
					pos = imgsearch.imagesearch("img/robot.png")
					if pos[0]<0 or pos[1]<0:
						continue
					hc.move((pos[0]-config["oth_mons"]+config["calibrate"],pos[1]+config["calibrate"]), 1)
					hc.click()
					robot = False
					#time.sleep(0.5)
					pos = imgsearch.imagesearch("img/wax_logo.png")
					if pos[0]<0 or pos[1]<0:
						continue
					hc.move((pos[0]-config["oth_mons"]+config["calibrate"],pos[1]+config["calibrate"]), 1)
					hc.click()
					approve = True
				elif config["mode"] == "cords":
					hc.move(config["cords"]["robot"],1)
					hc.click()
					robot = False
					hc.move(config["cords"]["miss"],1)
					hc.click()
					approve = True

			elif imgsearch.imagesearch("img/approve.png")[0] != -1 and approve:
				if config["mode"] == "auto":
					#print("approve")
					pos = imgsearch.imagesearch("img/approve.png")
					if pos[0]<0 or pos[1]<0:
						continue
					hc.move((pos[0]-config["oth_mons"]+config["calibrate"],pos[1]+config["calibrate"]),1)
					hc.click()
				elif config["mode"] == "cords":
					hc.move(config["cords"]["approve"],1)
					hc.click()

			#time.sleep(1)
			# Back to mining hub button
			elif imgsearch.imagesearch("img/go_to_hub.png")[0] != -1:
				if config["mode"] == "auto":
					#print("to hub")
					pos = imgsearch.imagesearch("img/go_to_hub.png")
					if pos[0]<0 or pos[1]<0:
						continue
					hc.move((pos[0]-config["oth_mons"]+config["calibrate"],pos[1]+config["calibrate"]), 1)
					hc.click()
					if tm.status():
						print("1 cycle: "+str(tm.stop())+"s")
					robot = True
				elif config["mode"] == "cords":
					hc.move(config["cords"]["mining hub"], 1)
					hc.click()
					if tm.status():
						print("1 cycle: "+str(tm.stop())+"s")
					robot = True

			#time.sleep(1)
			# Close error message button
			elif imgsearch.imagesearch("img/timed_out.png")[0] != -1:
				if config["mode"] == "auto":
					#print("error")
					pos = imgsearch.imagesearch("img/close.png")
					if pos[0]<0 or pos[1]<0:
						continue
					hc.move((pos[0]-config["oth_mons"]+config["calibrate"],pos[1]+config["calibrate"]), 1)
					hc.click()
					robot = True
				elif config["mode"] == "cords":
					hc.move(config["cords"]["error"], 1)
					hc.click()
					robot = True

			# Login button
			elif imgsearch.imagesearch("img/login.png")[0] != -1:
				if config["mode"] == "auto":
					#print("login")
					pos = imgsearch.imagesearch("img/login.png")
					if pos[0]<0 or pos[1]<0:
						continue
					hc.move((pos[0]-config["oth_mons"]+config["calibrate"],pos[1]+config["calibrate"]), 1)
					hc.click()
				elif config["mode"] == "cords":
					hc.move(config["cords"]["login"])
					hc.click

			# Second Mine button
			elif imgsearch.imagesearch("img/second_mine.png")[0] != -1:
				if config["mode"] == "auto":
					#print("second mine")
					pos = imgsearch.imagesearch("img/second_mine.png")
					if pos[0]<0 or pos[1]<0:
						continue
					hc.move((pos[0]-config["oth_mons"]+config["calibrate"],pos[1]+config["calibrate"]), 1)
					hc.click()
				elif config["mode"] == "cords":
					hc.move(config["cords"]["second_mine"])
					hc.click()

			# Second Claim button in mining hub
			elif imgsearch.imagesearch("img/second_claim.png")[0] != -1:
				if config["mode"] == "auto":
					#print("second claim")
					pos = imgsearch.imagesearch("img/second_claim.png")
					if pos[0]<0 or pos[1]<0:
						continue
					hc.move((pos[0]-config["oth_mons"]+config["calibrate"],pos[1]+config["calibrate"]), 1)
					hc.click()
				elif config["mode"] == "cords":
					hc.move(config["cords"]["second_claim"])
					hc.click()


		except Exception as e:
			print(e)
			print("Error!\nSaved to MainCrash.txt")
			with open("MainCrash.txt","w") as f:
				f.write("Crash Report\n\n"+str(e))
			if config["eoe"]: # EOE - exit on error
				sys.exit(0)



def on_press(key):
	# When F12 key is pressed, stop executing the script
	if key == keyboard.Key.f12:
		global exec_stop
		exec_stop = True
		print("Shutting down...")
		sys.exit(0)


def main():
	# Listen for pressed keys
	listener = keyboard.Listener(on_press=on_press)
	listener.start()
	run()


if __name__ == '__main__':
	main()
