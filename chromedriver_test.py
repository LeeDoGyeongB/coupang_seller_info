from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)


url_list = ['https://shop.coupang.com/A00179198','https://shop.coupang.com/A00179168','https://shop.coupang.com/A00156388', 'https://shop.coupang.com/A00179167', 'https://shop.coupang.com/A00179169']

# 데이터를 저장할 리스트를 만듭니다.
data_list = []

for url in url_list:
    # 웹페이지 해당 주소 이동
    driver.get(url)
    company_code = url.split('/')[-1]

    try:
        # 특정 버튼을 찾아 클릭
        button = driver.find_element(By.CSS_SELECTOR, 'button.clear-button.info-button.info-button')
        button.click()

        # 'table.detail' 요소가 로드될 때까지 최대 10초간 기다립니다.
        wait = WebDriverWait(driver, 10)
        table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.detail')))

        time.sleep(5)

        # 'table.detail' 요소 내의 모든 'tr' 요소를 찾습니다.
        row_elements = table.find_elements(By.TAG_NAME, 'tr')

        # 'seller' 변수의 내용을 '/' 기호를 기준으로 나눠 'company_name'과 'seller_name' 변수에 저장합니다.
        seller = row_elements[0].find_element(By.TAG_NAME, 'td').text
        company_name, seller_name = seller.split('/') if '/' in seller else (seller, '')

        contact_number = row_elements[1].find_element(By.TAG_NAME, 'td').text
        email = row_elements[2].find_element(By.TAG_NAME, 'td').text
        address = row_elements[3].find_element(By.TAG_NAME, 'td').text

        # 'seller_number' 변수의 내용에서 '-' 기호 삭제
        seller_number = row_elements[4].find_element(By.TAG_NAME, 'td').text.replace('-', '')

        # 데이터를 딕셔너리에 저장하고 리스트에 추가
        data = {
            'URL': url,
            'Company Code': company_code,
            'Company Name': company_name.strip(),
            'Seller Name': seller_name.strip(),
            'Contact Number': contact_number,
            'Email': email,
            'Address': address,
            'Seller Number': seller_number
        }
        data_list.append(data)

        time.sleep(1)

    except (TimeoutException, Exception):
        # 페이지가 로드되지 않는 경우, URL만 저장하고 다음 URL로 넘어갑니다.
        data = {
            'URL': url,
            'Company Code': company_code,
            'Company Name': '',
            'Seller Name': '',
            'Contact Number': '',
            'Email': '',
            'Address': '',
            'Seller Number': ''
        }
        data_list.append(data)

        time.sleep(1)

# 웹 브라우저 종료
driver.quit()

# 딕셔너리의 리스트를 CSV 파일로 저장
with open('coupang_seller_info.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=data.keys())
    writer.writeheader()
    for data in data_list:
        writer.writerow(data)