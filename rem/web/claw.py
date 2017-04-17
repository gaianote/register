from selenium import webdriver
import requests
from PIL import Image
import time
from .get_useragent import get_useragent
from .get_proxy_ip import get_proxy_ip
class Claw():
  """
  爬虫类，提供了一些方法用于更好的支持selenium
  """
  def __init__(self):
    pass
  def fake(self,type):
    UA = get_useragent(type)
    print(UA)
    options = webdriver.ChromeOptions()
    #IP = get_proxy_ip()
    #options.add_argument('--proxy-server=%s'%IP)
    if type == 'pc':
      options.add_argument('user-agent=%s'%UA)
      self.driver = webdriver.Chrome(chrome_options=options)
    elif type == 'phone':
      WIDTH = 320
      HEIGHT = 640
      PIXEL_RATIO = 3.0
      mobileEmulation = {"deviceMetrics": {"width": WIDTH, "height": HEIGHT, "pixelRatio": PIXEL_RATIO}, "userAgent": UA}
      options.add_experimental_option('mobileEmulation', mobileEmulation)
      self.driver = webdriver.Chrome(chrome_options=options)
      self.driver.set_window_size(WIDTH,HEIGHT)
  def get_phone_driver(self):
    print('ok')
    WIDTH = 320
    HEIGHT = 640
    PIXEL_RATIO = 3.0
    UA = 'Mozilla/5.0 (Linux; Android 4.1.1; GT-N7100 Build/JRO03C) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/6.3'
    mobileEmulation = {"deviceMetrics": {"width": WIDTH, "height": HEIGHT, "pixelRatio": PIXEL_RATIO}, "userAgent": UA}
    options = webdriver.ChromeOptions()
    options.add_experimental_option('mobileEmulation', mobileEmulation)
    self.driver = webdriver.Chrome(chrome_options=options)
    self.driver.set_window_size(WIDTH,HEIGHT+100)
  # 判断driver是否存在，不存在则启动driver;不输入参数则默认启动手机版驱动
  def get(self,url):
    if not hasattr(self,'driver'):
      self.driver = webdriver.Chrome()
    self.driver.get(url)
    self.wait_pageload()
  def query(self,parm):
    self.wait_pageload()
    # querySelectorAll使用的是' 诸如"[class_id='11']" 会出问题
    parm = parm.replace("'","\"")
    js = "document.querySelectorAll('%s');"%(parm)

    elem_list = self.run_js(js)
    # 一直寻找，知道找到元素为止
    for i in range(120):
      if elem_list != []:
        break
      time.sleep(1)
      elem_list = self.run_js(js)
    # 返回一个元素或者返回元素列表
    if len(elem_list) == 1:
      return elem_list[0]
    return elem_list
  def run_js(self,js):
    if js.find('return')== -1:
      js = 'return %s'%js
    result = self.driver.execute_script(js)
    return result
  def save_elemshot(self,css_selector,img_name):
    import os
    # 等待元素加载成功
    self.query(css_selector)
    js = """
    elem = document.querySelector('%s')
    res = elem.getBoundingClientRect()
    return res
    """%css_selector
    rect = self.run_js(js)
    self.driver.save_screenshot('screenshot.png')
    img = Image.open('screenshot.png')
    driver_width = self.run_js('window.innerWidth')
    pil_width = img.size[0]
    radio = pil_width/driver_width
    region = (rect['left']*radio,rect['top']*radio,rect['right']*radio,rect['bottom']*radio)
    img.crop(region).save(img_name)
    os.remove('screenshot.png')
  def wait_pageload(self):
    # 页面加载完成后再进行选择
    flag = True
    while flag:
      for i in range(120):
        time.sleep(1)
        js = "document.readyState == 'complete'"
        if self.run_js(js):
          flag = False
          break
      if flag:
        self.driver.refresh()

if __name__ == '__main__':
  pass