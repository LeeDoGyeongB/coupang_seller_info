import requests
import json
import pandas as pd
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

df = pd.read_csv('/Users/asst2401059/PycharmProjects/coupang_seller/coupang_vendorId.csv')
id_list = df.iloc[:, 0].tolist()
data_dict = {}

for i, id in enumerate(id_list, start=1):
    start_time = time.time()
    url = f'https://shop.coupang.com/api/v1/store/getStoreReview?urlName={id}'
    response = requests.get(url, verify=False)

    # JSON 형태의 문자열을 파싱합니다.
    data = json.loads(response.text)

    # 만약 vendorId가 존재하지 않는다면, '운영중지'로 대체
    if data['vendorId'] == '':
        data_dict[id] = {
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

        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"현재 {i}번째 url을 작업 중입니다. 이 작업을 진행하는 데 걸린 시간은 {elapsed_time}초입니다.")

    else:
        # 파싱한 결과를 딕셔너리에 저장합니다.
        data_dict[id] = data

        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"현재 {i}번째 url을 작업 중입니다. 이 작업을 진행하는 데 걸린 시간은 {elapsed_time}초입니다.")

new_data_dict = {}
for id, data in data_dict.items():
    new_data_dict[id] = {
        'vendorId': data['vendorId'],
        'ratingCount': data['ratingCount'],
        'thumbUpCount': data['thumbUpCount'],
        'thumbDownCount': data['thumbDownCount'],
        'thumbUpRatio': data['thumbUpRatio'],
        'name': data['name'],
        'repAddr1': data['repAddr1'],
        'repAddr2': data['repAddr2'],
        'repEmail': data['repEmail'],
        'repPersonName': data['repPersonName'],
        'repPhoneNum': data['repPhoneNum'],
        'businessNumber': data['businessNumber'].replace('-', ''),
        'sellerReviewDetailLink': data['sellerReviewDetailLink'],
    }

#  새로운 딕셔너리를 데이터프레임으로 변환합니다.
dict_df = pd.DataFrame(new_data_dict)

# 데이터프레임을 전치합니다.
dict_df = dict_df.transpose()

# 데이터프레임을 CSV 파일로 저장합니다.
dict_df.to_csv('data11.csv', encoding='utf-8')