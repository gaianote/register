def get_random_str(int):
  import random
  str = 'qwertyuiopasdfghjklzxcvbnm1234567890'
  arr = random.sample(str,int)
  return ''.join(arr)