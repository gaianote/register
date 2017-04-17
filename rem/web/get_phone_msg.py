import requests
# 文档 http://www.xingchenma.com:9180/httphelp.htm
def get_md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()

class Get_msg(object):
  def __init__(self,uname,upwd):
    self.uname = uname
    self.upwd = upwd
  def get_token(self):
    uname = self.uname
    upwd = get_md5(self.upwd).upper()
    payload = {'name':uname,'psw':upwd}
    url = 'http://www.xingchenma.com:9180/service.asmx/UserLoginStr'
    res = requests.get(url,params = payload)
    self.token = res.text
  def login_out(self):
    url = 'http://www.xingchenma.com:9180/service.asmx/UserExitStr?token=%s'%self.token
    res = requests.get(url)
  def get_phone_number(self,project_name):
    project_dic = {'bilibili':1471}
    self.project_id = project_dic[project_name]
    url = 'http://www.xingchenma.com:9180/service.asmx/GetHMStr'
    payload = {'token':self.token,'xmid':self.project_id,'sl':1,'lx':1,'a1':'','a2':'','pk':''}
    res = requests.get(url,params = payload)
    if 'hm'.find(res.text):
      self.phone_number = res.text[3:]
      print('获取号码成功，号码为:',res.text[3:])
    else
      print('系统繁忙')
  def get_msg(self):
    url = 'http://www.xingchenma.com:9180/service.asmx/GetYzmStr?token=string&hm=string&xmid=int'
    payload = {'token':self.token,'xmid':self.project_id,'hm'=self.phone_number}
    res = requests.get(url,params = payload)
    msg = res.text
    print(msg)
  def start(self):
    get_token()
    get_phone_number()
    return get_msg()

get_msg = Get_msg('gaianote','#^QH!@WLC6Xtc@').start

if __name__ == '__main__':
  get_msg('bilibili')
input()