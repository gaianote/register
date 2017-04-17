# 引入文字识别OCR SDK
from aip import AipOcr
class Ocr_baidu():
  def __init__(self):
    self.api_key = '7ILEoW5LC1X4mpSmzhz3NAG9'
    self.secret_key = 'wvHlMHf6BrL5yM8z9Qn8KTo7yqFzZPcp'
    self.api_id = '9476639'

  def get_access_token(self):
    baidu_api_url = 'https://aip.baidubce.com/oauth/2.0/token'
    payload = {'grant_type':'client_credentials',
    'client_id':self.api_key,
    'client_secret':self.secret_key
    }
    res = requests.post(baidu_api_url, params=payload)
    dic = json.loads(res.text)
    access_token = dic["access_token"]
    print(access_token)
  def ocr_baidu(self,filePath):
    # 初始化ApiOcr对象
    aipOcr = AipOcr(self.api_id, self.api_key, self.secret_key)
    # 读取图片
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    # 调用通用文字识别接口
    result = aipOcr.basicGeneral(get_file_content(filePath))
    return result

ocr_baidu = Ocr_baidu().ocr_baidu