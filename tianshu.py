import requests
import hashlib
import hmac
import base64
import time
import uuid
import random
  
# 生成流水号
def generate_serial_number():
    uid = uuid.uuid4()
    serial_number = uid.hex[:32]
    return serial_number
  
# 获取随机码
def generate_random_code(length=5):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    code = ""
    for _ in range(length):
        code += random.choice(characters)
    return code
  
# 生成签名和时间戳
def generate_signature(scene_id, request_path, app_secret, random_key):
    timestamp = str(int(time.time() * 1000))
    sign_string = f"{scene_id}&{timestamp}&{request_path}"
    secret_key = app_secret + random_key
    hmac_sha256 = hmac.new(
      secret_key.encode(), 
      sign_string.encode(),
      hashlib.sha256
    ).hexdigest().encode()
    signature = random_key + base64.b64encode(hmac_sha256).decode()
    return signature, timestamp
  
class AiHelperClient:
    def __init__(self, base_url, app_secret, scene_id):
        self.base_url = base_url
        self.app_secret = app_secret
        self.random_key = generate_random_code()
        self.scene_id = scene_id
        self.session = requests.Session()
  
    def post(self, endpoint, data):
        signature, timestamp = generate_signature(
            self.scene_id,
            endpoint,
            self.app_secret,
            self.random_key
        )
  
        url = f"{self.base_url}{endpoint}"
        headers = {
            'Content-Type': 'application/json',
            'x-signature': signature,
            'x-timestamp': timestamp
        }
  
        try:
            response = self.session.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return None