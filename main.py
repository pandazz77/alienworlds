import time

from worker import worker
import json


#load config
with open("config.json",encoding ="UTF-8") as jsonFile:
	config = json.load(jsonFile)
profiles = config["profiles"]
user_data_dir = config["user_data_dir"]

class workers_holder:
	def __init__(self,profiles,user_data_dir):
		self.profiles = profiles
		self.user_data_dir = user_data_dir
		self.workers = []
		self.load()

	def load(self):
		for profile in self.profiles:
			self.workers.append(worker(profile,{
				"calibrate":1,
				"waiter":0,
				"user_data_dir":self.user_data_dir,
				"set_up":False
				}))

	def run_all(self):
		for worker in self.workers:
			worker.start()
			time.sleep(2)

	def terminate_all(self):
		for worker in self.workers:
			worker.terminate()


if __name__ == "__main__":
	wh = workers_holder(profiles,user_data_dir)
	wh.run_all()


	"""
	w1 = worker("w1",{"calibrate":1,
		"waiter":3,
		"set_up":True})
	w1.start()
	"""