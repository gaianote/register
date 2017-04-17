import re
class Str_handle(object):
  """docstring for Str_handle"""
  def __init__(self):
    pass
  # 删除字符串内的标点符号
  def trim_punc(self,str):
    partten = "[\s+\.\!\\\|\/_,:;$%^*\?(+\"\'\[\]]+|[+——！，。：；“”‘’？、~@#￥%……&*（）]+|[()〔〕<>《》{}「」『』【】]+"
    return re.sub(partten,'',str)
str = Str_handle()