from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException

from pyvirtualdisplay import Display as PYDisplay
from os import popen
from time import sleep

def _driver_init():
  opts = webdriver.ChromeOptions()
  opts.binary_location = popen('which chromium').read().strip()
  driver = webdriver.Chrome(chrome_options=opts)
  return driver

def _driver_quit(d):
  d.quit()

class Display:
  def __init__(self,visible:bool=False)->None:
    self.display=None
    self.visible=visible
  def __enter__(self):
    self.display=PYDisplay(visible=(1 if self.visible else 0), size=(1024, 768))
    self.display.start()
    return self
  def __exit__(self, exc_type, exc_value, traceback):
    self.display.stop()

class Driver:
  def __init__(self):
    self.driver = None
    return
  def __enter__(self):
    self.driver = _driver_init()
    return self.driver
  def __exit__(self,exc_type, exc_value, traceback):
    _driver_quit(self.driver)

def test():
  """ Open display and samples chat messages """
  with Display(True) as disp, Driver() as driver:
    driver.get("https://habr.com/ru/company/jugru/blog/455936/")
    print('Im here')
    divs=driver.find_elements(By.XPATH,"//div");
    for div in divs:
      print(div, div.text)
