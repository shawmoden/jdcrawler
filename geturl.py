import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
chrome =webdriver.Chrome()
chrome.maximize_window()
chrome.get('https://passport.bilibili.com/login')
username =chrome.find_element_by_xpath("//input[@id='login-username']").send_keys("13100847952")
password =chrome.find_element_by_xpath("//input[@id='login-passwd']").send_keys("1234")
click =chrome.find_element_by_xpath("//a[@class='btn btn-login']").click()
chrome.implicitly_wait(5)
time.sleep(2)
img =chrome.find_element_by_xpath("//canvas[@class='geetest_canvas_bg geetest_absolute']")
full_img =chrome.find_element_by_xpath("//canvas[@class='geetest_canvas_fullbg geetest_fade geetest_absolute']")
# full_img =WebDriverWait(chrome,3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR("geetest_canvas_bg geetest_absolute"))))
img.screenshot('img.png')
full_img.screenshot('full_img.png')

