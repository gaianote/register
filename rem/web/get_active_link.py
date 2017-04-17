from .claw import Claw
import json
import time

class Get_active_link(Claw):

  def __init__(self,mail_uname,mail_upwd,mail_title):
    self.mail_uname = mail_uname.replace('@163.com','')
    self.mail_upwd = mail_upwd
    self.mail_title = mail_title
  def login_mail(self):
      elem = self.query('#pop_mailEntry')
      elem.click()
      self.query('#username').send_keys(self.mail_uname)
      self.query('#password').send_keys(self.mail_upwd)
      self.query('.loginBtn').click()
  def read_mail(self):
    self.query('.msgbox-hd.fn-alignCenter')
    self.query('.btn-inner')[1].click()
    # 寻找邮件标题''
    titles = self.query('.mail-list-subject')
    for title in titles:
      if title.text == self.mail_title:
        title.click()
        break
    # 得到激活链接，使用self.query确认邮件已加载
    self.active_link = self.query(".mRead-cont a")[2].get_attribute('href')

  def main(self):
    self.fake('phone')
    self.get('http://smart.mail.163.com/')
    self.login_mail()
    self.read_mail()
    self.driver.quit()
    return self.active_link

if __name__ == '__main__':
  print(Get_active_link('uus5h1x','yuanxi','【哔哩哔哩】会员邮件验证通知 请确认并完成绑定').main())
  input()