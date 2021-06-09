import pyautogui
import sys
import time
import python_imagesearch.imagesearch as imgsearch
from pyclick import HumanClicker
from pynput import keyboard
import json

#Сканируем файл с конфигом
with open("config.json",encoding ="UTF-8") as jsonFile:
	config = json.load(jsonFile)


exec_stop = False

def run():
	global config
	approve = False
	hc = HumanClicker()
	# While there's no 'execution stop' command passed
	while exec_stop is False:
		try:
			# Mine button
			if imgsearch.imagesearch("img/mine.png")[0] != -1:
				hc.move(config["cords"]["mine"], 1)
				hc.click()

			time.sleep(1)
			# Claim TLM button
			if imgsearch.imagesearch("img/claim.png")[0] != -1:
				hc.move(config["cords"]["claim"], 1)
				hc.click()

			# Authorize transaction button
			if imgsearch.imagesearch("img/captcha_solved.png")[0] != -1:
				hc.move(config["cords"]["captcha"], 1)
				hc.click()
				time.sleep(0.5)
				hc.move(config["cords"]["robot"],1)
				hc.click()
				time.sleep(0.5)
				hc.move(config["cords"]["miss"],1)
				hc.click()
				approve = True

			if imgsearch.imagesearch("img/approve.png")[0] != -1 and approve:
				hc.move(config["cords"]["approve"],1)
				hc.click()

			time.sleep(1)
			# Back to mining hub button
			if imgsearch.imagesearch("img/go_to_hub.png")[0] != -1:
				hc.move(config["cords"]["mining hub"], 1)
				hc.click()

			time.sleep(1)
			# Close error message button
			if imgsearch.imagesearch("img/timed_out.png")[0] != -1:
				hc.move(config["cords"]["error"], 1)
				hc.click()
		except:
			print("Error!\nSaved to MainCrash.txt")
			with open("MainCrash.txt","w") as f:
				f.write("Crash Report\n\n"+str(e))


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
