import json
import time
from json.decoder import JSONDecodeError

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from jd.cmd import kuandai

sku_id = '100016129312'


def getStock():
    url = 'https://item-soa.jd.com/getWareBusiness?callback=&skuId=' \
          + sku_id + '&cat=9987%2C653%2C655&area=1_2810_55530_0&shopId=1000004123&venderId=1000004123&paramJson=%7B' \
                     '%22platform2%22%3A%22100000000001%22%2C%22specialAttrStr%22%3A%22p0p1ppppppppp1p1ppppppp%22%2C' \
                     '%22skuMarkStr%22%3A%2200%22%7D&num=1 '
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/54.0.2840.99 Safari/537.36"
    }
    try:
        response = requests.get(url=url, headers=headers)
        res = json.loads(response.text)
        return res['stockInfo']['stockDesc']
    except JSONDecodeError:
        print('json解析失败')
        return '<strong>无货</strong>，此商品暂时售完'


driver = webdriver.Chrome(r'D:\SeleniumTest\webdriver\chromedriver.exe')
driver.get('https://cart.jd.com/cart/dynamic/gateForSubFlow.action?wids=' + sku_id + '&nums=1&subType=32')

flag = int(input('输入1确保登录和选择完毕：'))
if flag == 1:
    print('开始操作！')
    i = 0
    while True:
        i = i + 1
        if i == 100:
            driver.refresh()    # 防登录失效
            kuandai()
            i = 0
        begin = int(round(time.time() * 1000))
        time.sleep(0.03)
        var2 = getStock()
        end = int(round(time.time() * 1000))
        print(str(end - begin) + ' | ' + var2)
        if var2 != '<strong>无货</strong>，此商品暂时售完':
            driver.execute_script('submit_Order(null,2);')
            time.sleep(2)
            try:
                var3 = driver.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]').text
            except NoSuchElementException as e:
                var3 = driver.find_element_by_xpath('//*[@id="indexBlurId"]/div/div[1]/div[2]/div/div[1]/div[1]/div['
                                                    '1]/div/div[1]').text
            print(var3)
            if var3 == '抱歉，您购物车中的部分商品或者赠品暂时缺货，请结算其他商品':
                driver.get('https://cart.jd.com/cart/dynamic/gateForSubFlow.action?wids=' + sku_id + '&nums=1&subType=32')
            else:
                break
