import time

from worker import worker
import json


#load config
with open("config.json",encoding ="UTF-8") as jsonFile:
	config = json.load(jsonFile)
profiles = config["profiles"]

class workers_holder:
	def __init__(self,profiles):
		self.profiles = profiles
		self.workers = []
		self.load()

	def load(self):
		for profile in self.profiles:
			self.workers.append(worker(profile,{
				"calibrate":1,
				"waiter":0,
				"set_up":False
				}))

	def run_all(self):
		for worker in self.workers:
			worker.start()
			time.sleep(0)

	def terminate_all(self):
		for worker in self.workers:
			worker.terminate()


if __name__ == "__main__":
	wh = workers_holder(profiles)
	wh.run_all()


	"""
	w1 = worker("w1",{"calibrate":1,
		"waiter":3,
		"set_up":True})
	w1.start()
	"""