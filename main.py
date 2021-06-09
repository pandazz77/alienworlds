import time

from multiprocessing import Process

from worker import worker
import json


#load config
with open("config.json",encoding ="UTF-8") as jsonFile:
	config = json.load(jsonFile)
profiles = config["profiles"]

if __name__ == "__main__":
	procs = []

	for profile in profiles:
		proc = Process(target=worker,name=profile,args=(profile,{"calibrate":1,
		"waiter":config["waiter"],
		"set_up":config["set_up"],
		"hidden":config["hidden"],
		"window_size":config["window_size"],
		"chromium_path":config["chromium_path"],}))
		procs.append(proc)
		proc.start()
		time.sleep(config["profile_start_time"])
	
	for proc in procs:
		proc.join()
		#print(proc.name+" joined")



"""
w1 = worker("w1",{"calibrate":1,
	"waiter":3,
	"set_up":True})
w1.start()
"""