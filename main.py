from dati import dati
from register import register
# 这里的输入把子程序是输入截取了
order = input("""
请输入
1 答题
2 注册
""")

if order == '1':
  dati()
if order == '2':
  register()