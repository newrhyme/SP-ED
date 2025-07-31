import requests
import math
from datetime import datetime, timedelta
import urllib.parse

# 기상청 API Key
API_KEY = "fiIzvV1zTtuiM71dc57bLQ"

# 충북대 위치 (격자 좌표)
STN_ID = 131  

# 관측 시간 (1시간 단위 데이터)
now = datetime.now() - timedelta(hours=1)
tm = now.strftime("%Y%m%d%H")

url = "https://apihub.kma.go.kr/api/typ01/url/kma_sfctm2.php"
params = {
    "tm": tm,       # 관측 시간
    "stn": STN_ID,  # 관측소 번호
    "help": "0",
    "authKey": API_KEY
}

response = requests.get(url, params=params)

# 응답 확인
if response.status_code != 200:
    print("API 호출 실패:", response.status_code)
    print(response.text)
    exit()

# 데이터 파싱
lines = response.text.strip().split("\n")
header = lines[0].split()  # 첫 줄은 헤더
values = lines[1].split()  # 두 번째 줄은 실제 값

data = dict(zip(header, values))

temp = float(data["TA"])   # 기온(°C)
humid = float(data["HM"])  # 습도(%)
wind = float(data["WS"])   # 풍속(m/s)

# WBGT 근사 계산 (단순식)
Tw = temp * math.atan(0.151977 * math.sqrt(humid + 8.313659)) + \
     math.atan(temp + humid) - math.atan(humid - 1.676331) + \
     0.00391838 * humid ** 1.5 * math.atan(0.023101 * humid) - 4.686035
Tg = temp + 0.2 * (humid / 100 * 5)  # 단순 근사
WBGT = round(0.7 * Tw + 0.2 * Tg + 0.1 * temp, 2)

print(f"관측소: {STN_ID} (청주)")
print(f"현재 기온: {temp}°C")
print(f"현재 습도: {humid}%")
print(f"현재 풍속: {wind} m/s")
print(f"현재 WBGT: {WBGT}")