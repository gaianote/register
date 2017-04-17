import sqlite3
# 如果需要储存的字符本身含有 " 则需要注意
# 'cookie = \'%s\''%(cookie) cookie内部含有"" 必须用''
def run_sql(sql,fetch='fetchone'):
  conn = sqlite3.connect('account.db',timeout=10)
  cursor = conn.cursor()
  cursor.execute(sql)
  # 当num为传入参数时，num == ()
  if fetch == 'fetchone':
    result = cursor.fetchone()
  elif fetch == 'fetchall':
    result = cursor.fetchall()
  cursor.close()
  conn.commit()
  conn.close()
  return result

def export_to_text(table_name):
    sql = 'select uname,upwd from %s'%table_name
    for uname,upwd in run_sql(sql,'fetchall'):
      with open('galacg_account.txt', 'a+',encoding='UTF-8') as f:
        f.write('%s----%s\n'%(uname,upwd))