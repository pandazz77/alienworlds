from selenium.common.exceptions import MoveTargetOutOfBoundsException as selenium_exception
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth

from helium import *
from threading import Thread
import time
import cv2
import numpy as np
import sys


class worker(Thread):
	def __init__(self,name,args):
		Thread.__init__(self)
		self.name = name
		self.stop = False
		self.args = args

		self.calibrate = self.args["calibrate"]
		self.waiter = self.args["waiter"]
		self.set_up = self.args["set_up"]
		self.user_data_dir = self.args["user_data_dir"]


		self.options = webdriver.ChromeOptions()
		#brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
		#self.options.binary_location = brave_path
		#self.options.add_extension('extension.crx')
		self.options.add_argument("--enable-javascript")
		self.options.add_argument("--start-maximized")
		self.options.add_argument('window-size=1920x1080')#['--disable-web-security', '--user-data-dir', '--allow-running-insecure-content' ]

		self.options.add_argument("disable-infobars")
		#self.options.add_argument("--disable-extensions")
		self.options.add_argument("--disable-web-security")
		self.options.add_argument("--disable-blink-features")
		self.options.add_argument("--disable-blink-features=AutomationControlled")
		self.options.add_argument("--allow-running-insecure-content")
		self.options.add_argument('--disable-setuid-sandbox')
		

		self.options.add_argument('--headless')
		self.options.add_argument("--no-sandbox")
		self.options.add_experimental_option("useAutomationExtension", False)
		self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
		#self.options.add_experimental_option('w3c', False)
		self.options.add_argument(f"--user-data-dir={self.user_data_dir}")
		self.options.add_argument(f"profile-directory={self.name}")
		self.driver = webdriver.Chrome(executable_path = "chromedriver.exe",chrome_options=self.options,)
		self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
		self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
		stealth(self.driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
		set_driver(self.driver)
		#self.driver.maximize_window()
		#self.driver.set_window_size(1920, 1080)
		#self.ac = ActionChains(self.driver)

	def __str__(self):
		return "["+self.name+"] "

	def print(self,message):
		print("["+self.name+"] "+str(message))

	def run(self):
		self.print("runned")

		self.driver.get("https://play.alienworlds.io")
		if self.set_up:
			self.print("set up mode")
			time.sleep(9999)

		self.main_window = self.driver.window_handles[0]
		while self.stop is False:
			#self.print("working...")
			time.sleep(self.waiter)
			self.driver.save_screenshot(self.name+".png")

			if self.detect_picture(self.name+".png","img/login.png")[0]!=-1:
				try:
					self.print("login detected")
					coords = self.detect_picture(self.name+".png","img/login.png")
					#print(coords)
					click(Point(coords[0], coords[1]))
					self.login()
					time.sleep(1)
				except Exception as e:
					self.print(e)
					#time.sleep(3)

			elif self.detect_picture(self.name+".png","img/mine.png")[0]!=-1:
				self.print("mine detected")
				coords = self.detect_picture(self.name+".png","img/mine.png")
				#print(coords)
				click(Point(coords[0], coords[1]))

			elif self.detect_picture(self.name+".png","img/claim.png")[0]!=-1:
				self.print("claim detected")
				coords = self.detect_picture(self.name+".png","img/claim.png")
				#print(coords)
				click(Point(coords[0], coords[1]))
				self.captcha_process()

			elif self.detect_picture(self.name+".png","img/go_to_hub.png")[0]!=-1:
				self.print("mining hub detected")
				coords = self.detect_picture(self.name+".png","img/go_to_hub.png")
				#print(coords)
				click(Point(coords[0], coords[1]))

			elif self.detect_picture(self.name+".png","img/second_claim.png")[0]!=-1:
				self.print("second claim detected")
				coords = self.detect_picture(self.name+".png","img/second_claim.png")
				#print(coords)
				click(Point(coords[0], coords[1]))
				self.captcha_process()

			elif self.detect_picture(self.name+".png","img/second_mine.png")[0]!=-1:
				self.print("second mine detected")
				coords = self.detect_picture(self.name+".png","img/second_mine.png")
				#print(coords)
				click(Point(coords[0], coords[1]))

			elif self.detect_picture(self.name+".png","img/mine_in_menu.png")[0]!=-1:
				self.print("mine_in_menu detected")
				coords = self.detect_picture(self.name+".png","img/mine_in_menu.png")
				#print(coords)
				click(Point(coords[0], coords[1]))

		return

	def terminate(self):
		self.stop = True

	def captcha_process(self):
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
		return

	def login(self):
		self.main_window = self.driver.window_handles[0]
		for t in range(15):
			self.driver.save_screenshot(f"login{self.name}.png")
			time.sleep(1)
			try:
				self.driver.switch_to_window(self.driver.window_handles[1])
				time.sleep(2)
				self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[5]/div/div/div/div[1]/div[1]/input").send_keys("modenov.aleshenka@mail.ru")
				self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[5]/div/div/div/div[1]/div[2]/input").send_keys("qX556qEklaB@")
				self.driver.switch_to_window(self.driver.window_handles[0])
				self.driver.save_screenshot("1.png")
				self.driver.switch_to_window(self.driver.window_handles[1])
				self.driver.save_screenshot("2.png")
				self.driver.switch_to_window(self.driver.window_handles[2])
				self.driver.save_screenshot("3.png")
				self.driver.switch_to_window(self.driver.window_handles[1])
				for t in range(60):
					try:
						self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[5]/div/div/div/div[5]/button[1]').click()
					except:
						break
					self.driver.save_screenshot("3.png")
					time.sleep(1)

				time.sleep(2)
				self.driver.save_screenshot("4.png")
				self.print(self.driver.window_handles)
				self.driver.switch_to_window(self.main_window)
				self.print("window 1 logined")
				break
			except Exception as e:
				self.print(e)
			time.sleep(1)
			try:
				self.driver.switch_to_window(self.driver.window_handles[2])
				time.sleep(2)
				self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[5]/div/div/div/div[1]/div[1]/input").send_keys("modenov.aleshenka@mail.ru")
				self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[5]/div/div/div/div[1]/div[2]/input").send_keys("qX556qEklaB@")
				self.driver.switch_to_window(self.driver.window_handles[0])
				self.driver.save_screenshot("1.png")
				self.driver.switch_to_window(self.driver.window_handles[1])
				self.driver.save_screenshot("2.png")
				self.driver.switch_to_window(self.driver.window_handles[2])
				self.driver.save_screenshot("3.png")
				for t in range(60):
					try:
						self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[5]/div/div/div/div[5]/button[1]').click()
					except:
						break
					self.driver.save_screenshot("3.png")
					time.sleep(1)
				time.sleep(1)

				time.sleep(2)
				self.driver.save_screenshot("4.png")
				#print(self.driver.page_source)

				#time.sleep(10)
				#self.print(self.driver.window_handles)
				self.driver.switch_to_window(self.main_window)
				self.print("window 2 logined")
				break
			except Exception as e:
				self.print(e)
		self.print("returned to main window")
		return


			#print(coords)

	def detect_picture(self,img,img_template):
		try:
			#self.print("detecting...")
			#print(img_template)
			img_rgb = cv2.imread(img)
			img_gray = cv2.cvtColor(img_rgb,cv2.COLOR_BGR2GRAY)
			template = cv2.imread(img_template,0)
			w, h = template.shape[::-1]

			res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
			#print(res)
			threshold = 0.8
			loc = np.where(res>=threshold)
			#print("loc: ",loc)
			"""
			for pt in zip(*loc[::-1]):
				print("coords: ",pt[0]+w,pt[1]+h)
			"""
			if len(loc[0])>0:
				return (loc[1][0]+self.calibrate,loc[0][0]+self.calibrate)
			else:
				return (-1,-1)
		except Exception as e:
			self.print("detect picture exception: "+str(e))
			return (-1,-1)