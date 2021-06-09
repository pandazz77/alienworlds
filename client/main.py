import time
from cfg import *

from client import client

from multiprocessing import Process

from worker import worker
import json

from info import print_info


#load config
with open("config.json",encoding ="UTF-8") as jsonFile:
	config = json.load(jsonFile)
profiles = config["profiles"]

if __name__ == "__main__":
	cl = client(server_ip,server_port,config["key"],version)
	cl.start()

	print_info(config)

	while True:
		print(cl.message)
		if cl.get_access():
			break
		time.sleep(1)


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