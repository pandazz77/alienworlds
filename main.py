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

user32 = ctypes.windll.user32
c_screensize = int(user32.GetSystemMetrics(0)/2), int(user32.GetSystemMetrics(1)/2)

controller = keyboard.Controller()

exec_stop = False

def run():
	global config
	global screensize
	global controller

	tm = Timer() # Mine timer
	c_tm = Timer() #Claiming timer
	m_tm = Timer() #Mining timer

	hc = HumanClicker()
	#Farm mode
	print("Watcher started [farm]")
	while exec_stop is False:
		for cord in config["cords"]["farm_cords"]:
			farm_attempt = 0
			while farm_attempt<config["farm_attempt_limit"] and exec_stop is False:
				#print("c_tm status: ",c_tm.status())
				#print("m_tm status: ",m_tm.status())
				#print("FA: "+str(farm_attempt))
				try:
					#Claiming error timer handler
					if c_tm.status():
						#print("c_tm time: ",c_tm.get_time())
						if c_tm.get_time()>config["claiming_timer_limit"]:
							print("Claiming timer>config_time\nRestarting page")
							pos = imgsearch.imagesearch("img/deny.png")
							if pos[0]>0 or pos[1]>0:
								hc.move((pos[0]-config["oth_mons"]+config["calibrate"],pos[1]+config["calibrate"]), 1)
								hc.click()
							hc.move(c_screensize,1)
							hc.click()
							farm_attempt = 0
							controller.press(keyboard.Key.f5)
							controller.release(keyboard.Key.f5)
							time.sleep(2)
							c_tm.stop()

					if m_tm.status():
						#print("m_tm time: ",m_tm.get_time())
						if m_tm.get_time()>config["mining_timer_limit"]:
							print("Mining progress timer>config_time\nRestarting page")
							hc.move(c_screensize,1)
							hc.click()
							farm_attempt = 0
							controller.press(keyboard.Key.f5)
							controller.release(keyboard.Key.f5)
							time.sleep(2)
							m_tm.stop()

					#Claiming timer starting
					if imgsearch.imagesearch("img/claiming.png")[0] != -1 or imgsearch.imagesearch("img/claiming2.png")[0] != -1:
						#print("claiming found")
						farm_attempt = 0
						if c_tm.status() is False:
							#print("starting c_tm")
							c_tm.start()
					else:
						if c_tm.status():
							#print("stopping c_tm")
							c_tm.stop()

					#Mining timer starting
					if imgsearch.imagesearch("img/mining_progress.png")[0] != -1:
						#print("mining found")
						farm_attempt = 0
						if m_tm.status() is False:
							#print("starting m_tm")
							m_tm.start()
					else:
						if m_tm.status():
							#print("stop m_tm")
							m_tm.stop()


					# Mine button
					if imgsearch.imagesearch("img/mine.png")[0] != -1:
						pos = imgsearch.imagesearch("img/mine.png")
						if pos[0]<0 or pos[1]<0:
							continue
						hc.move((pos[0]-config["oth_mons"]+config["calibrate"],pos[1]+config["calibrate"]), 1)
						hc.click()
						farm_attempt = 0

					# Claim TLM button
					elif imgsearch.imagesearch("img/claim.png")[0] != -1 and imgsearch.imagesearch("img/clime_false.png")[0] == -1:
						pos =  imgsearch.imagesearch("img/claim.png")
						if pos[0]<0 or pos[1]<0:
							continue
						hc.move((pos[0]-config["oth_mons"]+config["calibrate"],pos[1]+config["calibrate"]), 1)
						hc.click()
						farm_attempt = 0

					if imgsearch.imagesearch("img/approve.png")[0] != -1:
						pos = imgsearch.imagesearch("img/approve.png")
						if pos[0]<0 or pos[1]<0:
							continue
						hc.move((pos[0]-config["oth_mons"]+config["calibrate"],pos[1]+config["calibrate"]),1)
						hc.click()
						farm_attempt = 0

					# Back to mining hub button
					elif imgsearch.imagesearch("img/go_to_hub.png")[0] != -1:
						pos = imgsearch.imagesearch("img/go_to_hub.png")
						if pos[0]<0 or pos[1]<0:
							continue
						hc.move((pos[0]-config["oth_mons"]+config["calibrate"],pos[1]+config["calibrate"]), 1)
						hc.click()
						farm_attempt = 0

					# Close error message button
					elif imgsearch.imagesearch("img/timed_out.png")[0] != -1:
						pos = imgsearch.imagesearch("img/close.png")
						if pos[0]<0 or pos[1]<0:
							continue
						hc.move((pos[0]-config["oth_mons"]+config["calibrate"],pos[1]+config["calibrate"]), 1)
						hc.click()
						farm_attempt = 0

					# Login button
					elif imgsearch.imagesearch("img/login.png")[0] != -1:
						pos = imgsearch.imagesearch("img/login.png")
						if pos[0]<0 or pos[1]<0:
							continue
						hc.move((pos[0]-config["oth_mons"]+config["calibrate"],pos[1]+config["calibrate"]), 1)
						hc.click()
						farm_attempt = 0

					# Second Mine button
					elif imgsearch.imagesearch("img/second_mine.png")[0] != -1:
						pos = imgsearch.imagesearch("img/second_mine.png")
						if pos[0]<0 or pos[1]<0:
							continue
						hc.move((pos[0]-config["oth_mons"]+config["calibrate"],pos[1]+config["calibrate"]), 1)
						hc.click()
						farm_attempt = 0

					# Second Claim button in mining hub
					elif imgsearch.imagesearch("img/second_claim.png")[0] != -1:
						pos = imgsearch.imagesearch("img/second_claim.png")
						if pos[0]<0 or pos[1]<0:
							continue
						hc.move((pos[0]-config["oth_mons"]+config["calibrate"],pos[1]+config["calibrate"]), 1)
						hc.click()
						farm_attempt = 0

				except Exception as e:
					print(e)
					print("Error!\nSaved to MainCrash.txt")
					with open("MainCrash.txt","w") as f:
						f.write("Crash Report\n\n"+str(e))
					if config["eoe"]: # EOE - exit on error
						sys.exit(0)

				farm_attempt+=1

			if exec_stop:
				break

			hc.move(cord,1)
			hc.click()



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
