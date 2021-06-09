#Modules browsers
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from helium import *

import time

#Modules for images detect
import cv2
import numpy as np
import sys, os


class worker:
	def __init__(self,name,args):
		self.name = name
		self.stop = False
		self.args = args

		self.calibrate = self.args["calibrate"]
		self.waiter = self.args["waiter"]
		self.set_up = self.args["set_up"]
		self.hidden = self.args["hidden"]
		self.window_size = self.args["window_size"]
		self.chromium_path = self.args["chromium_path"]


		self.options = webdriver.ChromeOptions()
		if self.chromium_path!="":
			self.options.binary_location = self.chromium_path
		self.options.add_argument("--enable-javascript")
		if self.set_up:
			self.options.add_argument("--start-maximized")
		self.options.add_argument(f'window-size={self.window_size}')

		self.options.add_argument("--disable-infobars")
		self.options.add_argument("--log-level=3")
		self.options.add_argument("--disable-web-security")
		self.options.add_argument("--disable-blink-features")
		self.options.add_argument("--disable-blink-features=AutomationControlled")
		self.options.add_argument("--allow-running-insecure-content")
		
		self.options.add_experimental_option("useAutomationExtension", False)
		self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
		self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
		self.options.add_argument(f"--user-data-dir={os.getcwd()}\\profiles\\{self.name}")
		self.driver = webdriver.Chrome(executable_path = "chromedriver.exe",chrome_options=self.options,)
		if self.hidden:
			self.driver.set_window_position(-10000,0)
		set_driver(self.driver) # for helium
		self.run()

	def __str__(self):
		return "["+self.name+"] "

	def print(self,message):
		print(self.__str__()+str(message))
		sys.stdout.flush() #Multiprocessing требует перенаправлять поток на вывод после каждого print

	def run(self):
		self.print("runned")

		self.driver.get("https://play.alienworlds.io")
		if self.set_up:
			self.print("set up mode")

		self.main_window = self.driver.window_handles[0]
		while self.stop is False:
			time.sleep(self.waiter)

			self.driver.switch_to_window(self.main_window)

			try:
				self.driver.save_screenshot(self.name+".png")
			except Exception as e:
				self.print("exception in save screenshot: "+str(e))

			if self.detect_picture(self.name+".png","img/login.png")[0]!=-1:
				try:
					self.print("login detected")
					coords = self.detect_picture(self.name+".png","img/login.png")
					click(Point(coords[0], coords[1]))
					time.sleep(1)
				except Exception as e:
					self.print("exception in login: "+str(e))
					time.sleep(3)

			elif self.detect_picture(self.name+".png","img/error.png")[0]!=-1:
				self.print("error detected")
				coords = self.detect_picture(self.name+".png","img/close.png")
				click(Point(coords[0], coords[1]))

			elif self.detect_picture(self.name+".png","img/mine.png")[0]!=-1:
				self.print("mine detected")
				coords = self.detect_picture(self.name+".png","img/mine.png")
				click(Point(coords[0], coords[1]))

			elif self.detect_picture(self.name+".png","img/claim.png")[0]!=-1 and self.detect_picture(self.name+".png","img/clime_false.png")[0]==-1:
				self.print("claim detected")
				coords = self.detect_picture(self.name+".png","img/claim.png")
				click(Point(coords[0], coords[1]))
				self.captcha_process()

			elif self.detect_picture(self.name+".png","img/go_to_hub.png")[0]!=-1:
				self.print("mining hub detected")
				coords = self.detect_picture(self.name+".png","img/go_to_hub.png")
				click(Point(coords[0], coords[1]))

			elif self.detect_picture(self.name+".png","img/second_claim.png")[0]!=-1 and self.detect_picture(self.name+".png","img/clime_false.png")[0]==-1:
				self.print("second claim detected")
				coords = self.detect_picture(self.name+".png","img/second_claim.png")
				click(Point(coords[0], coords[1]))
				self.captcha_process()

			elif self.detect_picture(self.name+".png","img/second_mine.png")[0]!=-1:
				self.print("second mine detected")
				coords = self.detect_picture(self.name+".png","img/second_mine.png")
				click(Point(coords[0], coords[1]))

			elif self.detect_picture(self.name+".png","img/mine_in_menu.png")[0]!=-1:
				self.print("mine_in_menu detected")
				coords = self.detect_picture(self.name+".png","img/mine_in_menu.png")
				click(Point(coords[0], coords[1]))

		return

	def terminate(self):
		self.stop = True

	def captcha_process(self):
		try:
			self.main_window = self.driver.window_handles[0]
			time.sleep(2)
			self.driver.switch_to_window(self.driver.window_handles[1])
			for t in range(180):
				try:
					self.driver.find_element_by_class_name('button-text').click()
					self.driver.switch_to_window(self.main_window)
					break
				except:
					pass
				time.sleep(1)
		except Exception as e:
			self.print("exception in captcha_process: "+str(e))
		return

	def detect_picture(self,img,img_template):
		try:
			img_rgb = cv2.imread(img)
			img_gray = cv2.cvtColor(img_rgb,cv2.COLOR_BGR2GRAY)
			template = cv2.imread(img_template,0)
			w, h = template.shape[::-1]

			res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
			threshold = 0.8
			loc = np.where(res>=threshold)
			if len(loc[0])>0:
				return (loc[1][0]+self.calibrate,loc[0][0]+self.calibrate)
			else:
				return (-1,-1)
		except Exception as e:
			self.print("detect picture exception: "+str(e))
			return (-1,-1)