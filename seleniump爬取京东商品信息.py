# selenium爬取京东商品信息

import csv
import time

from lxml import etree
# 第一步：导入库
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# 第二步：声明浏览器对象
web = webdriver.Chrome()

# 第三步：打开京东网页
web.get("https://www.jd.com/")
web.maximize_window()  # 窗口最大化

# 第四步：找到搜索框，输入搜索词,按回车
web.find_element_by_xpath('//*[@id="key"]').send_keys('键盘', Keys.ENTER)
time.sleep(1)  # 等待

# 第五步：分析页面，爬取商品信息，保存在csv中
# 首先打开一个CSV文件
with open("goods_data3.csv", "w+", newline='', encoding='utf-8') as csvfile:
    # csvfile.write(codecs.BOM_UTF8)  ##存入表内的文字格式
    writer = csv.writer(csvfile)  # 存入表时所使用的格式
    writer.writerow(['name', 'price'])
    page_count = 0
    all_page = 10
    while page_count < all_page:
        page_count += 1
        print('正在爬取第%d页' % page_count)
        # 首先通过分析页面发现商品数据是动态加载出来的，所以要将滚动条拖到最下面，才能加载出所有商品信息
        js = "var q=document.documentElement.scrollTop=" + str(5000)
        web.execute_script(js)
        time.sleep(1)
        # 获取网页页面源码，遍历所有的商品信息
        page = web.page_source
        doc = etree.HTML(str(page))
        links = doc.xpath('//*[@id="J_goodsList"]/ul/li')
        count = 0
        for link in links:
            count = count + 1
            print('当前正在爬取第%d项商品' % count)
            name = link.xpath('./div/div[3]/a/em/text()')
            price = link.xpath('./div/div[2]/strong/i/text()')
            # print(name[0],price[0])
            try:
                # 写入文件
                writer.writerow([name[0].strip(), price[0]])  # 写入表
            except:
                print('该项产品信息有误')
                continue
        # 翻页
        web.find_element_by_xpath('//*[@id="J_bottomPage"]/span[1]/a[9]').click()
        time.sleep(5)

time.sleep(10)
# 最后一步：关闭浏览器
web.close()
web.quit()
