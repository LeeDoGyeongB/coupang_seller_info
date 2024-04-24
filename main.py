# 필요 모듈 import
import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

df = pd.read_csv('/Users/asst2401059/PycharmProjects/coupang_seller/coupang_seller_added_240311.csv', header=None)

# 중복 데이터 제거
df = df.drop_duplicates(['index'], keep='first')
df = df.reset_index(drop=True)

# 필요없는 컬럼 삭제
df = df.drop([2, 3, 4, 5, 13], axis=1)

# '운영중지'상태인 row만 보이기
new_df = df[df[1] == '운영중지']
new_df = new_df.reset_index(drop=True)

# 해당 컬럼을 리스트(seller_id_list)로 저장
seller_id_list = new_df[0].tolist()

sample_dict = {}
data_dict = {}

# CSV 파일 초기화
with open('coupang_seller_added_result.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['vendorId', 'name', 'repAddr1', 'repAddr2', 'repEmail', 'repPersonName', 'repPhoneNum', 'businessNumber'])

for i, seller_id in enumerate(seller_id_list, start=1):
    start_time = time.time()

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://shop.coupang.com',
        'Referer': f'https://shop.coupang.com/{seller_id}?locale=ko_KR&platform=p',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    json_data = {
        'vendorId': f'{seller_id}',
        'source': 'direct',
        'enableAdultItemDisplay': True,
        'nextPageKey': 0,
        'filter': 'SORT_KEY:',
    }
    response = requests.post('https://shop.coupang.com/api/v1/listing', headers=headers, json=json_data, verify=False)

    try:
        data_dict = json.loads(response.text)

        products = data_dict['data']['products']
        if not products:
            pass
        else:
            product_info = products[0]
            vendorItemId = product_info['vendorItemId']
            productId = product_info['productId']
            itemId = product_info['itemId']

            info_url = f'https://www.coupang.com/vp/products/{productId}/items/{itemId}/vendoritems/{vendorItemId}'
            response = requests.get(info_url, headers=headers, verify=False)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # 소스코드 형태인 soup을 딕셔너리로 변환
                data = json.loads(soup.text)

                # 판매자 정보 딕셔너리만 가져오기
                seller_detail = data['returnPolicyVo']['sellerDetailInfo']

                sample_dict[seller_id] = {
                    'vendorId': seller_id,
                    'name': seller_detail['vendorName'],
                    'repAddr1': seller_detail['repAddress1'],
                    'repAddr2': seller_detail['repAddress2'],
                    'repEmail': seller_detail['repEmail'],
                    'repPersonName': seller_detail['repPersonName'],
                    'repPhoneNum': seller_detail['repPhoneNum'],
                    'businessNumber': seller_detail['bizNum']
                    }

    except ValueError:
        pass

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"현재 {i}번째 url(vednorId: {seller_id})을 작업 중입니다. 소요 시간은 {elapsed_time}초입니다.")

    # 새로운 딕셔너리를 데이터프레임으로 변환합니다.
    sample_dict = pd.DataFrame.from_dict(sample_dict, orient='index')

    # 데이터프레임을 CSV 파일에 추가합니다.
    sample_dict.to_csv('coupang_seller_added_result.csv', mode='a', header=False, encoding='utf-8')

    # 딕셔너리를 초기화합니다.
    sample_dict = {}