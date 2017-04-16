import rem
import json
import time

class Register(rem.Claw):
  def __init__(self):
    self.mail_title = '【哔哩哔哩】会员邮件验证通知 请确认并完成绑定'
  def start(self):
    sql = 'select mail_uname,mail_upwd from mail_163 where site_name is NULL'
    if rem.run_sql(sql) == None:
      print('已经没有可用邮箱，请补充...')
      input()
    self.mail_uname,self.mail_upwd = rem.run_sql(sql)
    self.url = 'https://passport.bilibili.com/register/mail'
    self.get(self.url)
    self.fill_form()
  def fill_form(self):
    self.query("input[name='uname']").send_keys(self.mail_uname)
    self.query('#vdCodeTxt').click()
    self.query('#agree').click()
    # 可能验证码错误或者不响应
    self.save_elemshot('#captchaImg','img/captcha.png')
    capcha = rem.dmt.decode('img/captcha.png',43)
    self.query('#vdCodeTxt').send_keys(capcha)
    time.sleep(1)
    self.query('#emailStn').click()
    if self.query('.header .hd'):
      print('已发送激活链接')
      self.active_link = rem.Get_active_link(self.mail_uname,self.mail_upwd,self.mail_title).main()
      self.fill_site_info()
    elif self.query('#emailStn'):
      print('此账号异常...')
      sql = 'update mail_163 set site_name = "ERROR" where mail_uname = "%s"'%self.mail_uname
      rem.run_sql(sql)
  # 填写bilibil用户名与密码
  def fill_site_info(self):
    print('填写网站信息')
    self.get(self.active_link)
    uname = rem.get_uname()
    upwd = self.mail_upwd
    self.query("input[name='uname']").send_keys(uname)
    self.query("input[name='userpwd']").send_keys(upwd)
    print('查看用户名是否被注册')
    while True:
      time.sleep(3)
      if self.query("#unameError").text == "":
        break
      else:
        uname = rem.get_uname()
        self.query("input[name='uname']").clear()
        self.query("input[name='uname']").send_keys(uname)
        self.query("input[name='userpwd']").click()
    self.query("input[type='submit']").click()
    # 如果显示注册成功页面，保存数据到数据库
    if self.query(".reg-complete-wrapper"):
      print ('正在存储内容')

      sql = 'update mail_163 set site_name = "bilibili" where mail_uname ="%s"'%self.mail_uname
      rem.run_sql(sql)

      cookie = self.driver.get_cookies()
      cookie = json.dumps(cookie)
      sql = 'insert into bilibili (mail_uname,mail_upwd,cookie) values (\'%s\',\'%s\',\'%s\')'%(self.mail_uname,self.mail_upwd,cookie)
      rem.run_sql(sql)
    self.driver.quit()

####注册几个账号就执行几次

while True:
  try:
    rem.adsl.reconnect()
    register = Register()
    register.start()
  except Exception as e:
    register.driver.quit()
    print(e)
