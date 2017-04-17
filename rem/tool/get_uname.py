from .sql import run_sql
def get_uname():
 sql = 'select uname from uname_box where is_used is Null'
 uname, = run_sql(sql)
 sql = 'update uname_box set is_used = "Ture" where uname = "%s"'%uname
 run_sql(sql)
 print(uname)
 return uname