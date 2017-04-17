import rem
def _add_account(mail_uname,mail_upwd):
  sql = '''CREATE TABLE IF NOT EXISTS MAIL_163(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        MAIL_UNAME TEXT,
        MAIL_UPWD TEXT,
        SITE_NAME TEXT)'''
  rem.run_sql(sql)
  # 查询是否插入过该邮箱，如果没有，则插入数据库
  sql = 'select * from mail_163 where mail_uname = "%s"'%(mail_uname)
  result = rem.run_sql(sql)
  if(result == None):
    # 插入用户名 密码等
    sql = 'insert into mail_163 (mail_uname,mail_upwd) values ("%s","%s")'%(mail_uname,mail_upwd)
    rem.run_sql(sql)
    print ("%s插入成功..."%mail_uname)
  else:
    print ('已经插入过此邮箱%s...'%mail_uname)

def add_accounts(filename,separator):
  with open(filename,'r') as f:
    for line in f.readlines():
      mail_account = line.strip().split(separator)
      mail_uname = mail_account[0]
      mail_upwd = mail_account[1]
      _add_account(mail_uname,mail_upwd)

###################################################################

add_accounts('account.txt','----')

sql = 'select * from mail_163'
print(rem.run_sql(sql,'fetchall'))
input()