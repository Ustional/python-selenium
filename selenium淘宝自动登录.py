import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ChromeOptions, ActionChains


# 定义爬取单页的函数
def get_page(web):
    divs = web.find_elements_by_xpath('//*[@id="mainsrp-itemlist"]/div/div/div[1]/div')
    # print(divs)
    for div in divs:
        info = div.find_element_by_xpath('./div[2]/div[2]/a').text  # 商品名称
        price = div.find_element_by_xpath('./div[2]/div[1]/div[1]/strong').text + '元'  # 商品价格
        deal = div.find_element_by_xpath('./div[2]/div[1]/div[2]').text  # 商品付款人数
        name = div.find_element_by_xpath('./div[2]/div[3]/div[1]/a/span[2]').text  # 商家店名
        print(info, price, deal, name, sep="|")
        try:
            csvwriter.writerow([info, price, deal, name])
        except :
            pass


option = ChromeOptions()
# 设置为开发者模式，防止被各大网站识别出来使用了Selenium
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_argument("--disable-blink-features")
option.add_argument("--disable-blink-features=AutomationControlled")
# 初始化一个web对象
web = webdriver.Chrome(options=option)
# 进入淘宝官网
web.get('https://www.taobao.com/')
# 点击登录
web.find_element_by_xpath('//*[@id="J_SiteNavLogin"]/div[1]/div[1]/a[1]').click()
# 输入账号密码
web.find_element_by_xpath('//*[@id="fm-login-id"]').send_keys('17347593420')
web.find_element_by_xpath('//*[@id="fm-login-password"]').send_keys('sui1756224213...')
# 点击登录
web.find_element_by_xpath('//*[@id="login-form"]/div[4]/button').click()
time.sleep(2)
# 搜索商品并回车
web.find_element_by_xpath('//*[@id="q"]').send_keys('电脑', Keys.ENTER)
time.sleep(3)
#  验证淘宝滑块，在前三秒也可以手动滑块，因为不确保自动滑块能成功
try:
    yz = web.find_element_by_xpath('//*[@id="baxia-punish"]/div[2]/div/div[1]/div[2]/div/p').text
    if yz == '通过验证以确保正常访问':
        while 1:
            # 获取滑块的大小
            span_background = web.find_element_by_xpath('//*[@id="nc_1__scale_text"]/span')
            span_background_size = span_background.size
            # print(span_background_size)
            # 获取滑块的位置
            button = web.find_element_by_xpath('//*[@id="nc_1_n1z"]')
            button_location = button.location
            # print(button_location)
            # 拖动操作：drag_and_drop_by_offset
            # 将滑块的位置由初始位置，右移一个滑动条长度（即为x坐标在滑块位置基础上，加上滑动条的长度，y坐标保持滑块的坐标位置）
            x_location = span_background_size["width"]
            y_location = button_location["y"]
            # print(x_location, y_location)
            action = ActionChains(web)
            source = web.find_element_by_xpath('//*[@id="nc_1_n1z"]')
            action.click_and_hold(source).perform()
            action.move_by_offset(x_location, 0)
            action.release().perform()
            time.sleep(1)
            try:
                web.find_element_by_xpath('//*[@id="`nc_1_refresh1`"]').click()
                time.sleep(3)
            except:
                pass
except:
    with open('taobao.csv', mode='a', newline='', encoding='gbk') as fp:
        csvwriter = csv.writer(fp, delimiter=',')
        csvwriter.writerow(['info', 'price', 'deal', 'name'])
    Allpage = 3
    count = 0
    while count < Allpage:
        count += 1
        print('-------------------正在爬取第%d页---------------------' % count)
        get_page(web)
        web.find_element_by_xpath('//*[@id="mainsrp-pager"]/div/div/div/ul/li[8]/a/span[1]').click()
        print('------------------------')
        time.sleep(5)

    web.close()
    web.quit()

# with open('taobao.csv', mode='a', newline='', encoding='gbk') as fp:
#     csvwriter = csv.writer(fp, delimiter=',')
#     csvwriter.writerow(['info', 'price', 'deal', 'name'])
# Allpage = 3
# count = 0
# while count < Allpage:
#     count += 1
#     print('-------------------正在爬取第%d页---------------------' % count)
#     get_page(web)
#     web.find_element_by_xpath('//*[@id="mainsrp-pager"]/div/div/div/ul/li[8]/a/span[1]').click()
#     print('------------------------')
#     time.sleep(5)
#
# web.close()
# web.quit()
