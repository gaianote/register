import requests
import time
import re
def md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str.encode('utf8'))
    return m.hexdigest()

class Xingchenma(object):
  def __init__(self, name,pwd):
    self.name = name
    self.pwd = pwd
    self.api = {
    'base_url':'http://www.xingchenma.com:9180/service.asmx/',
    'login':'UserLoginStr',
    'exit':'UserExitStr',
    'hm':'GetHMStr',
    'msg':'GetYzmStr'
    }
  def get_token(self):
    name = self.name
    pwd = md5(self.pwd).upper()
    url = self.api['base_url'] + self.api['login']
    payload = {'name':name,'psw':pwd}
    res = requests.get(url,params = payload)
    return res.text
  def get_phone_number(self,xmid):
    # bilibili 1471 网易 65 知乎 1280
    #xmid：项目id lx：获得号码数量
    self.token = self.get_token()
    payload={'token':self.token,'xmid' : xmid,'sl' : 1,'lx' : 1,'a1' : '','a2' : '','pk' : ''}
    url = self.api['base_url'] + self.api['hm']
    res =requests.get(url,params = payload)
    self.phone_number = res.text[3:]
    self.xmid = xmid
    return res.text[3:]
  def get_phone_msg(self):
    for i in range(120):
      payload={'token':self.token,'hm':self.phone_number,'xmid' : self.xmid}
      url = self.api['base_url'] + self.api['msg']
      res =requests.get(url,params = payload)
      if len(res.text)>=6:
        return re.findall('\d{6}',res.text)[0]
      time.sleep(1)
    return False

xcm = Xingchenma('gaianote','#^QH!@WLC6Xtc@')
