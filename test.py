from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("user-data-dir=C:\\Users\\Pandazz\\AppData\\Local\\Google\\Chrome\\User Data")

options.add_argument("--profile-directory=Profile 1") # add another profile path

driver = webdriver.Chrome(executable_path=r'chromedriver.exe', options=options)
#//*[@id="google-social-btn"]
driver.get("https://play.alienworlds.io")
while True:
	time.sleep(3)
	try:
		driver.switch_to_window(driver.window_handles[1])
		driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[4]/div[1]/div[2]/button/div/img').click()
		break
	except Exception as e:
		print(e)
	time.sleep(3)
	try:
		driver.switch_to_window(driver.window_handles[2])
		driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[4]/div[1]/div[2]/button/div/img').click()
		break
	except Exception as e:
		print(e)
