import time
import os

class Adsl(object):
  def __init__(self):
    # 分别填写adsl名称，用户名与密码，dsl名称一般为宽带连接
    self.name = "宽带连接"
    self.username = 'ADSL'
    self.password = '123456'
  def connect(self):
    cmd_str = "rasdial %s %s %s" % (self.name, self.username, self.password)
    os.system(cmd_str)
    time.sleep(5)
  def disconnect(self):
    cmd_str = "rasdial %s /disconnect" % self.name
    os.system(cmd_str)
    time.sleep(5)
  def reconnect(self):
    self.disconnect()
    self.connect()

adsl = Adsl()