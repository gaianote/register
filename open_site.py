import os
import time

import rem

main_menu = """
########################## 指挥官，网页登录助手竭诚为您服务 ####################
请输入以下指令打开相应的网站
1. 打开星辰网打码平台
2.
"""
class Open_site(rem.Claw):
  """docstring for Open"""
  def __init__(self):
    pass
  def main_menu(self):
    i=os.system('cls')
    print(main_menu)
    order = input('请输入指令: ')
    if order == '1':
      self.login_xingchenma()
  def login_xingchenma(self):
    self.get('http://www.xingchenma.com:9000/')
    self.query('#yhmc').send_keys('gaianote')
    self.query('#psw').send_keys('#^QH!@WLC6Xtc@')
    input('等待退出')
if __name__ == '__main__':
  Open_site().main_menu()