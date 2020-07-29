import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def get_content(request_url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html = requests.get(request_url, headers=headers, timeout=10)
    content = html.text
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    return soup


def get_auto_info(soup):

    table = soup.find('div', class_='search-result-list')
    name_list = table.find_all(class_='cx-name text-hover')
    price_list = table.find_all(class_='cx-price')
    photolink_list = table.find_all(class_='img')
    df = pd.DataFrame(columns=['名称', '最低价格（万）', '最高价格（万）', '产品图片链接'])
    for i in range(len(name_list)):
        item = {}
        item['名称'] = name_list[i].text
        price = price_list[i].text
        if price == "暂无" or price == "24.08万" or price == "30.18万" or price == "14.89万":
            item['最低价格（万）'] = price
            item['最高价格（万）'] = price
        else:
            item['最低价格（万）'] = float(price.split('-')[0])
            item['最高价格（万）'] = float(price.split('-')[1][:-1])
        item['产品图片链接'] = photolink_list[i]['src']
        df = df.append(item, ignore_index=True)
    return df


def main():
    page_num = 3
    base_url = 'http://car.bitauto.com/xuanchegongju/?mid=8'
    result = pd.DataFrame(columns=['名称', '最低价格（万）', '最高价格（万）', '产品图片链接'])

    for i in range(page_num):
        request_url = base_url + '&page=' + str(i+1)
        soup = get_content(request_url)
        df = get_auto_info(soup)
        result = result.append(df, ignore_index=True)
    print(result)
    result.to_csv('大众品牌汽车信息.csv', index=False, encoding='utf_8_sig')


if __name__ == "__main__":
    main()