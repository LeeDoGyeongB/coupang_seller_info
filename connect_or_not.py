# 필요 모듈 import
import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 전체 데이터의 url의 정보가 담긴 csv 파일 열기
df = pd.read_csv('/Users/asst2401059/PycharmProjects/coupang_seller/url_connect_3.csv')

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
result_dict = {}

with open('connect_result_added.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['url', 'store_id', 'status'])

for idx, row in df.iterrows():
    url = row['store_url']
    store_id = row['id']
    try:
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            if soup.text == '':
                result_dict[url] = {
                    'url': url,
                    'store_id': store_id,
                    'status': '판매 중지'
                }
                time.sleep(1)
            else:
                result_dict[url] = {
                    'url': url,
                    'store_id': store_id,
                    'status': ''
                }
                time.sleep(1)
            print(f'{idx}번째 데이터 수집 완료 / id : {store_id}')
        else:
            print(f"Request failed with status code {response.status_code}. Stopping the loop.")
            break
    except Exception as e:
        print(e)

    df = pd.DataFrame.from_dict(result_dict, orient='index')
    df.to_csv('connect_result_added.csv', mode='a', header=False, encoding='utf-8')
    result_dict = {}
