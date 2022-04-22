import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

web = webdriver.Chrome()
# 获得网页
web.get('https://www.lagou.com/')
# 窗口最大化
web.maximize_window()
# 点击切换城市
web.find_element_by_xpath('//*[@id="changeCityBox"]/ul/li[1]/a').click()
time.sleep(3)
# 点击登录按钮
web.find_element_by_xpath('//*[@id="lg_tbar"]/div[1]/div[2]/ul/li[1]/a').click()
# 点击切换密码登录
web.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[2]/div[3]/div[2]/div[1]/div[1]').click()
time.sleep(3)  # 停留3秒
# 输入框输入用户名和密码
web.find_element_by_xpath(
    '/html/body/div[2]/div[1]/div/div/div[2]/div[3]/div[1]/div/div[1]/form/div[1]/div/input').send_keys('17347593420')
web.find_element_by_xpath(
    '/html/body/div[2]/div[1]/div/div/div[2]/div[3]/div[1]/div/div[1]/form/div[2]/div/input').send_keys(
    'Sui1756224213...')
# 点击同意用户协议
web.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[2]/div[3]/div[5]/div[2]/img[1]').click()
# 点击登录按钮
web.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[2]/div[3]/div[2]/div[2]/div[2]').click()
time.sleep(10)  # 停留10秒时间自己验证
# 搜索框输入搜索关键词，按回车键
web.find_element_by_xpath('//*[@id="search_input"]').send_keys('python', Keys.ENTER)
time.sleep(5)
# 循环爬取30页
# 首先打开一个CSV文件
with open("post.csv", "w+", encoding='utf-8') as csvfile:
    # csvfile.write(codecs.BOM_UTF8)  ##存入表内的文字格式
    writer = csv.writer(csvfile)  # 存入表时所使用的格式
    writer.writerow(['name', 'price', 'company_name', 'post_condition'])

    count = 0
    all_page = 30
    while count < all_page:
        count += 1
        print('-------------------第%d页-------------------' % count)
        # print('正在爬取第%d页' % count)
        divs = web.find_elements_by_xpath('//*[@id="jobList"]/div[1]/div')
        # /html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[1]/div[1]
        # 第二步：遍历每一个div
        for div in divs:
            # 获取岗位名称
            name = div.find_element_by_xpath('./div[1]/div[1]/div[1]/a').text
            name = name.split('[')[0]
            # 获取公司名称
            company_name = div.find_element_by_xpath('./div[1]/div[2]/div[1]/a').text
            # 获取薪资水平
            price = div.find_element_by_xpath('./div[1]/div[1]/div[2]/span').text
            # 获取岗位要求
            post_condition = div.find_element_by_xpath('./div[1]/div[1]/div[2]').text
            post_condition = post_condition.split('k')[2]
            print(name, price, company_name, post_condition)
            # 写入文件
            writer.writerow([name, price, company_name, post_condition])  # 写入表
        # 翻页
        web.find_element_by_xpath('//*[@id="jobList"]/div[3]/ul/li[last()]/a').click()
        time.sleep(5)

'''
count = 0
while count <= 30:
    count += 1
    print('正在爬取第%d页'%count)
    a = []
    for i in range(1, 16):
        table = web.find_element_by_xpath('//div[@class="list__YibNq"]/div[{}]'.format(i))
        a.append(table.text)
    for t in range(15):
        print(a[t])
        print('-----------------------------------------------')
    web.find_element_by_xpath('//ul[@class="lg-pagination"]/li[last()]/a').click()
    time.sleep(5)
'''
# 关闭浏览器
web.close()
web.quit()
