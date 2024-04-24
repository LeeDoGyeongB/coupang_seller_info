import requests
import json
import pandas as pd
import csv
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

df = pd.read_csv('/Users/asst2401059/PycharmProjects/coupang_seller/coupang_new_db(240311).csv')
id_list = df.iloc[:, 0].tolist()
data_dict = {}

# CSV 파일 초기화
with open('coupang_seller_add.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['vendorId', 'ratingCount', 'thumbUpCount', 'thumbDownCount', 'thumbUpRatio', 'name', 'repAddr1', 'repAddr2', 'repEmail', 'repPersonName', 'repPhoneNum', 'businessNumber', 'sellerReviewDetailLink'])

for i, url_id in enumerate(id_list, start=1):
    start_time = time.time()
    url = f'https://shop.coupang.com/api/v1/store/getStoreReview?urlName={url_id}'
    response = requests.get(url, verify=False)

    # JSON 형태의 문자열을 파싱합니다.
    data = json.loads(response.text)

    if data['vendorId'] == '':
        data_dict[url_id] = {
            'vendorId': '운영중지',
            'ratingCount': '',
            'thumbUpCount': '',
            'thumbDownCount': '',
            'thumbUpRatio': '',
            'name': '',
            'repAddr1': '',
            'repAddr2': '',
            'repEmail': '',
            'repPersonName': '',
            'repPhoneNum': '',
            'businessNumber': '',
            'sellerReviewDetailLink': ''
        }

    else:
        # 파싱한 결과를 딕셔너리에 저장합니다.
        data_dict[url_id] = data

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"현재 {i}번째 url을 작업 중입니다. 이 작업을 진행하는 데 걸린 시간은 {elapsed_time}초입니다.")

    # 새로운 딕셔너리를 데이터프레임으로 변환합니다.
    dict_df = pd.DataFrame.from_dict(data_dict, orient='index')

    # 데이터프레임을 CSV 파일에 추가합니다.
    dict_df.to_csv('coupang_seller_added_240311.csv', mode='a', header=False, encoding='utf-8')

    # 딕셔너리를 초기화합니다.
    data_dict = {}