import re
import yaml

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

URL_DEF="https://habr.com/ru/company/jugru/blog/455936/"

def run(url:str=URL_DEF):
  """ Open display and samples chat messages """
  fname=re.sub('[^\w\s]', '_', url)+".yaml"
  with Display(True) as disp, Driver() as driver:
    print('Navigating to', url)
    driver.get(url)
    print('Searching elements')
    divs=driver.find_elements(By.XPATH,"//div")
    print('Dumping...')
    page=[]
    for i,div in enumerate(divs):
      # page.append({'id':div.id, 'rect':div.rect, 'inner':div.get_attribute('innerHTML')})
      page.append({'id':div.id, 'rect':div.rect, 'text':div.text})
      if i%10 == 0:
        print(i)
    with open(fname,'w') as f:
      yaml.dump(page,f)
    print('Done, check', fname)
    return fname




