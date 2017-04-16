import rem
import time
from random import choice
class Baidu_master(rem.Claw):
  def __init__(self, keyword,title,hits):
    self.keyword = keyword
    self.title = title
    self.hits = hits
    self.get_hits_list()
    self.hour_lock = -1
  def random_sleep(self,start_time,sleep_time):
    sleep_time = choice(range(start_time,sleep_time))
    time.sleep(sleep_time)

  def random_scroll(self):
    random = choice(range(3,10))
    for i in range(random):
      random = choice(range(10))/10
      self.run_js('window.scrollTo(0, document.body.scrollHeight*%s)'%random)
      self.random_sleep(2,6)
  def get_rank(self):
    self.search_title()
    rank = 0
    while True:
      for title in self.query('h3 a'):
        rank += 1
        if title.text ==self.title:
          height = title.location_once_scrolled_into_view
          print('当前排名是:',rank)
          return
      self.run_js('window.scrollTo(0, document.body.scrollHeight)')
      self.driver.find_element_by_link_text("下一页>").click()
  def get_hits_list(self):
    # hits是24小时内的总点击数，取正整数，使点击数在24小时内随机分布
    day_hits = int(self.hits*4/5)
    night_hits = self.hits - day_hits
    hits_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(day_hits):
      time = choice(range(8,24))
      hits_list[time] += 1
    for i in range(night_hits):
      time = choice(range(0,8))
      hits_list[time] += 1
    self.hits_list = hits_list
    print(self.hits_list)
  def start(self):
    #rem.adsl.reconnect()
    self.search_title()
    self.find_title()
    self.driver.quit()
  def main(self):
    self.random_sleep(0,1)
    # 得到当前整点数
    hour = int(time.strftime('%H'))
    # 每日凌晨0点重新更新点击时段分布
    if hour == 0:
      self.get_hits_list()
    # 每小时获取一次点击列表
    if hour != self.hour_lock:
      self.hour_lock = hour
      task_count = self.hits_list[hour]
    # 主程序运行区
    if task_count > 0:
      print(hour,task_count)
      self.start()
      task_count -= 1
class Baidu_pc_master(Baidu_master):
  def search_title(self):
    self.fake('pc')
    self.get('https://www.baidu.com')
    self.random_sleep(1,5)
    self.query('#kw').send_keys('汤不热')
    self.random_sleep(1,5)
    self.query('#kw').send_keys('账号')
    self.random_sleep(1,5)
    self.query('#su').click()
    self.random_sleep(10,30)
  def find_title(self):
    for i in range(10):
      self.random_scroll()
      for title in self.query('h3 a'):
        if title.text ==self.title:
          height = title.location_once_scrolled_into_view
          print(height)
          self.run_js('window.scrollTo(0, %s)'%height)
          title.click()
          self.random_sleep(50,60)
          return
      self.run_js('window.scrollTo(0, document.body.scrollHeight)')
      self.driver.find_element_by_link_text("下一页>").click()
      self.random_sleep(20,30)

class Baidu_phone_master(Baidu_master):
  def search_title(self):
    self.fake('phone')
    self.get('https://www.baidu.com')
    self.random_sleep(1,5)
    self.query('#index-kw').send_keys('汤不热')
    self.random_sleep(1,5)
    self.query('#index-kw').send_keys('账号')
    self.random_sleep(1,5)
    self.query('#index-bn').click()
    self.random_sleep(10,30)
    #page-controller a
  def find_title(self):
    is_first_page = True
    for i in range(10):
      self.random_scroll()
      for title in self.query('h3'):
        if title.text ==self.title:
          height = title.location_once_scrolled_into_view
          print(height)
          self.run_js('window.scrollTo(0, %s)'%height)
          title.click()
          self.random_sleep(50,60)
          return
      self.run_js('window.scrollTo(0, document.body.scrollHeight)')
      if is_first_page:
        self.query('#page-controller a').click()
        is_first_page = False
      else:
        self.query('.new-pagenav-right a').click()
      self.random_sleep(20,30)

keyword = '汤不热账号'
title = '汤不热账号交易 | tumblr 汤不热账号24小时自动发货'
hits = 100
'''

'''
baidu_pc_master = Baidu_pc_master(keyword,title,hits)
baidu_phone_master = Baidu_phone_master(keyword,title,hits)
while True:
  baidu_pc_master.main()
  baidu_phone_master.main()







'''
instagram账号
TOP终于开通个人Instagram账号啦!!赶快去关注吧!_BigBang全球资讯...
http://www.haokoo.com/else/2753983.html
第4页 第2名
32-33名 2017-4-13
23名 2017-4-14
'''