import rem
import json
import time


def register():
  uname = rem.get_uname()
  upwd = rem.get_random_str(6)
  phone_number = rem.xcm.get_phone_number(1471)
  claw = rem.Claw()
  url = 'https://passport.bilibili.com/register/phone'
  claw.get(url)
  claw.query('[name="uname"]').send_keys(uname)
  while True:
    claw.query('#password').click()
    time.sleep(3)
    if claw.query("#unameTip").text == "":
      break
    else:
      uname = rem.get_uname()
      claw.query('[name="uname"]').clear()
      claw.query('[name="uname"]').send_keys(uname)
  claw.query('#password').send_keys(upwd)
  claw.query('#new_phone').send_keys(phone_number)
  claw.query('#getCaptch').click()
  # 输入图片验证码
  claw.save_elemshot('#captchaImg','img/captcha.png')
  captcha = rem.dmt.decode('img/captcha.png',43)
  claw.query('.d-content #yzm').send_keys(captcha)
  claw.query('input[value="确定"]').click()

  # 输入短信验证码
  phone_number_msg = rem.xcm.get_phone_msg()
  if not phone_number_msg:
    return False
  claw.query('.new_phone #yzm').send_keys(phone_number_msg)
  claw.query('#agree').click()
  claw.query('#regSubmit').click()
  if claw.query('.reg-complete-wrapper'):
    cookie = claw.driver.get_cookies()
    cookie = json.dumps(cookie)
    sql = 'insert into bilibili (uname,upwd,phone_number,cookie,level) values (\'%s\',\'%s\',\'%s\',\'%s\',0)'%(uname,upwd,phone_number,cookie)
    rem.run_sql(sql)
    print(uname,upwd,phone_number,'all_clear')
  claw.driver.quit()
if __name__ == '__main__':
  for i in range(10):
    register()
