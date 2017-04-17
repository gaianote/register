class Io_handle(object):
  """docstring for Io_handle"""
  def __init__(self):
    pass
  # w+ 重写文件，如果没有则创建文件
  def write(self,filename,str):
    with open(filename, 'w+',encoding='UTF-8') as f:
      f.write(str)
  # a+ 追加写文件，如果没有则创建文件
  def writelines(self,filename,str):
    with open(filename, 'a+',encoding='UTF-8') as f:
        f.write(str)
  # 逐行读文本
  def readlines(self,filename,callback):
    with open(filename,'r', encoding='UTF-8') as f:
      for line in f.readlines():
        callback(line)

io = Io_handle()