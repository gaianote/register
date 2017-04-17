import time
import re
import difflib
import operator
import rem
import json
class Bilibili_dati(rem.Claw):
    def __init__ (self):
      self.mail_title = '【哔哩哔哩】会员邮件验证通知 请确认并完成绑定'
    def dati(self):
      sql = 'select phone_number,upwd from bilibili where level < 1'
      self.phone_number,self.upwd = rem.run_sql(sql)
      #sql = 'update mail_163 set site_level = 50 where mail_uname = "%s"'%self.mail_uname
      #rem.run_sql(sql)
      self.login_bilibili()
      self.get('https://account.bilibili.com/answer/base')
      if self.run_js('document.location.href') == "https://account.bilibili.com/answer/promotion":
        self._dati_zixuan()
      else:
        self._dati_liyi()
        self._dati_zixuan()
      self.driver.quit()

    def _dati_liyi(self):
      self.query('.examListBox .solution')
      js ="""
      var qus = document.querySelectorAll('.examListBox .solution');
      for(i=0;i<qus.length;i++){
        qus[i].querySelectorAll('li')[0].click()
      };
      document.querySelector('.enterBut.enterButdefault').click();
      """
      self.driver.execute_script(js)
      self.query('.d-button.d-state-highlight').click()
      time.sleep(5)
      for i in range(1,4):
        self.query('.examLi.error')
        js ="""
        var qus = document.querySelectorAll('.examLi.error');
        for(i=0;i<qus.length;i++){
          qus[i].querySelectorAll('li')[%d].click()
        };
        document.querySelector('.enterBut.enterButdefault').click();
        """%i
        self.driver.execute_script(js)
        time.sleep(60)
        if self.query('.d-button.d-state-highlight'):
          self.query('.d-button.d-state-highlight').click()
    def _dati_zixuan(self):
        sql = 'select qus,ans from BILIBILI_QUS_BANK'
        self.BILIBILI_QUS_BANK = rem.run_sql(sql,'fetchall')
        # 选择答题类型
        self.query("[class_id='11']").click()
        self.query("[class_id='12']").click()
        self.query("[class_id='13']").click()
        time.sleep(1)
        self.query('.enterButdefault').click()
        self.query('#examListUl .examLi')
        ##################  识别图像 ########################
        self.driver.set_window_size(730, 400)
        time.sleep(5)

        for i in range(60):
          time.sleep(10)
          ############ 截图并得到百度返回的结果 #################
          js ="""
          var qus = document.querySelectorAll('#examListUl .examLi');
          qus[%d].scrollIntoView()
          """%i
          screenshot_path = "img/%d.png"%i
          self.driver.execute_script(js)
          self.driver.save_screenshot(screenshot_path)
          result = rem.ocr_baidu(screenshot_path)
          try:
            result = result['words_result']
            ############ 处理百度返回的结果 #################
            pointer = 0
            ratio = {}
            for words in result:
              #{'words': 'CC给了鲁鲁修??'}
              words = words['words']
              if pointer == 0:
                qus = rem.str.trim_punc(words)
                qus = re.sub('^\d{1,2}','',qus)
                correct_ans = self.get_ans(qus)
                if correct_ans == None:
                  rem.io.writelines('bilibili_qus.txt','%s\n'%qus)
                  print(qus,'题库中无此题...')
                  break
                print('########【原始问题以及答案】##########')
                print(qus,correct_ans)
              else:
                ans = rem.str.trim_punc(words)
                ans = re.sub('^[ABCD]','',ans)
                print(ans)
                ratio[pointer] = difflib.SequenceMatcher(None, correct_ans, ans).ratio()
                if ans == correct_ans:
                  js ="""
                  var qus = document.querySelectorAll('#examListUl .examLi');
                  qus[%d].querySelectorAll('.solution li')[%d].click()
                  """%(i,pointer-1)
                  self.driver.execute_script(js)
                  break
              pointer += 1
            print(ratio)
            sorted_ratio = sorted(ratio.items(), key=operator.itemgetter(1))
            pointer = sorted_ratio[-1][0]
            print(i,pointer)
            js ="""
            var qus = document.querySelectorAll('#examListUl .examLi');
            qus[%d].querySelectorAll('.solution li')[%d].click()
            """%(i,pointer-1)
            self.driver.execute_script(js)

          except Exception as e:
            print(e)
            print('不会就选c')
            js ="""
            var qus = document.querySelectorAll('#examListUl .examLi');
            qus[%d].querySelectorAll('.solution li')[2].click()
            """%i
            self.driver.execute_script(js)

        input('等待验证码')
        if self.query('.resultDeRight'):
            sql = 'update bilibili set level = 1 where phone_number = "%s"'%self.phone_number
            rem.run_sql(sql)
            print('保存数据成功！')
        elif self.query('.cardButton.oneMoreTime'):
          print('答题失败了')

    def get_ans(self,qus):
      for qus_data,ans_data in self.BILIBILI_QUS_BANK:
        ratio = difflib.SequenceMatcher(None, qus, qus_data).ratio()
        if ratio >= 0.8:
          print('【猜测问题为：%s】'%qus_data)
          return ans_data
    def daily_task(self):
        # 得到登录日期，如果登录日期不是今日就进行每日任务
        date = time.strftime('%Y-%d-%m')
        sql = 'select mail_uname from mail_163 where site_name = "bilibili" and login_date is not "%s"'%date
        self.mail_uname = rem.run_sql(sql)
        self.get('http://www.bilibili.com/')
        self.get_cookie()
        # 看视频
        self.query('.v-item a')
        js = "document.querySelector('.v-item a').href"
        href = self.run_js(js)
        self.get(href)
        # 关注up主
        time.sleep(2)
        if self.query('.b-btn.f').text == "+ 关注":
          print(self.query('.b-btn.f').text)
          self.query('.b-btn.f').click()
        # 投硬币
        self.query('.b-icon-anim-coin').click()
        self.query('.b-btn.ok').click()
        self.set_cookie()
        sql = 'update mail_163 set login_date = "%s" where mail_uname = "%s"'%(date,self.mail_uname)
        rem.run_sql(sql)
        print('每日任务完成...')
        input()
    def login_bilibili(self):
      self.get('http://www.bilibili.com/')
      self.get_cookie()
      js = "document.querySelector('#i_menu_login_reg').style.display"
      display = self.run_js(js)
      if display == 'list-item':
        self.get('https://passport.bilibili.com/login')
        while self.driver.current_url == 'https://passport.bilibili.com/login':
          mail = '%s@163.com'%self.mail_uname
          self.query('#userIdTxt').send_keys(mail)
          self.query('#passwdTxt').send_keys(self.mail_upwd)
          self.query('#vdCodeTxt').click()
          capcha_src = 'https://passport.bilibili.com/captcha'
          capcha = self.get_capcha(capcha_src)
          self.query('#vdCodeTxt').send_keys(capcha)
          self.query("input[class ='login'").click()
          time.sleep(1)
          self.get('http://www.bilibili.com/')
          self.set_cookie()
          self.driver.refresh()
    def get_cookie(self):
      sql = "select cookie from bilibili where phone_number = '%s'"%self.phone_number
      cookies, = rem.run_sql(sql)
      if cookies:
        cookies = json.loads(cookies)
        for cookie in cookies:
          self.driver.add_cookie(cookie)
        self.driver.refresh()
        return True
      else:
        return False


dati = Bilibili_dati().dati
if __name__ == '__main__':
  dati()