import rem
sql = '''CREATE TABLE IF NOT EXISTS BILIBILI(
      ID INTEGER PRIMARY KEY AUTOINCREMENT,
      MAIL_UNAME TEXT,
      MAIL_UPWD TEXT,
      COOKIE TEXT,
      LEVEl TEXT,
      PROJECT_NAME TEXT,
      LOGIN_DATE TEXT)'''
rem.run_sql(sql)
print('ok')
input()