# -*- coding: utf-8 -*-
import rem
import json

class Get_name(rem.Claw):
  """docstring for Get_name"""
  def __init__(self):
    pass
  def get_name(self):
    self.get('http://www.qmsjmfb.com/jp.php')
    self.query('.name_box')
    js = '''
    jp_str = 'あアいイうウえエおオあアあアいイiうッウuえ々エeおオoかカかカkaきキkiくクkuけケkeこコkoさサさサsaしシshiすスsuせセseそソsoたタたタtaちチchiつツtsuてテteとトtoなナなナnaにニniぬヌnuねネneのノnoはハはハhaひヒhiふフfuへヘheほホhoまマまマmaみミmiむムmuめメmeもモmoやヤやヤyaゆユyuよヨyoらラらラraりリriるルruれレreろロroわワわワwa　 をヲwoんンn　がガがガgaぎギgiぐグguげゲgeごゴgoざザざザzaじジjiずズzuぜゼzeぞゾzoだダだダdaぢヂjiづヅzuでデdeどドdoばバばバbaびビbiぶブbuべベbeぼボboぱパぱパpaぴピpiぷプpuぺペpeぽポpo　  やヤゆユよヨかカきゃキャkyaきゅキュkyuきょキョkyoがガぎゃギャgyaぎゅギュgyuぎょギョgyoさサしゃシャshaしゅシュshuしょショshoざザじゃジャjyaじゅジュjyuじょジョjyoたタちゃチャchaちゅチュchuちょチョchoだダ ぢゃヂャdya ぢゅヂュdyu ぢょヂョdyoなナにゃニャnyaにゅニュnyuにょニョnyoはハひゃヒャhyaひゅヒュhyuひょヒョhyoばバびゃビャbyaびゅビュbyuびょビョbyoぱパぴゃピャpyaぴゅピュpyuぴょピョpyoまマみゃミャmyaみゅミュmyuみょミョmyoらラりゃリャryaりゅリュryuりょリョryo'
    jp_str_dic =jp_str.split('')
    elem = document.querySelectorAll('li');
    name_box = [];
    for (var i=0;i<elem.length;i++){
      var has_jp_str = false;
      start = elem[i].innerText.indexOf('(')+1
      end = elem[i].innerText.indexOf(')')
      name = elem[i].innerText.substring(start,end)
      for(var j=0;j<jp_str_dic.length;j++){
        if (name.indexOf(jp_str_dic[j]) !== -1){
          has_jp_str = true;
          break;
        }
      }
      if (!has_jp_str){
        name_box.push(name)
      }
    };
    return JSON.stringify(name_box)
    '''
    self.name_box = json.loads(self.run_js(js))

  def save_data(self):
    sql = '''CREATE TABLE IF NOT EXISTS UNAME_BOX(
          ID INTEGER PRIMARY KEY AUTOINCREMENT,
          UNAME TEXT,
          TYPE TEXT,
          GENDER TEXT,
          IS_USED TEXT)
          '''
    rem.run_sql(sql)
    for i in range(len(self.name_box)):
      uname = self.name_box[i]
      type = 'japan'
      sql = 'select * from uname_box where uname = "%s"'%(uname)
      result = rem.run_sql(sql)
      if(result == None):
        # 插入用户名 密码等
        sql = 'insert into uname_box (uname,type) values ("%s","%s")'%(uname,type)
        rem.run_sql(sql)
        print ("%s插入成功..."%uname)
      else:
        print ('已经插入过此内容')
    print ('插入完成')
    self.driver.quit()
  def start(self):
    self.get_name()
    self.save_data()

get_name = Get_name()
for i in range(1):
  get_name.start()