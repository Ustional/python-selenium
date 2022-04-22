from selenium import webdriver
from lxml import etree
import time
import csv

# 初始化一个web对象
web = webdriver.Chrome()
# 进入CSDN官网
web.get('https://www.csdn.net/')
# 点击人工智能
web.find_element_by_xpath('//*[@id="floor-nav_557"]/div/div/div/ul/li[7]/a').click()


# 爬取单页函数
def get_page(html):
    html = etree.HTML(html)
    table = html.xpath('//div[@class="Community"]/div')
    count = 0
    for t in table:
        count += 1
        print('正在爬取第%d' % count)
        name = t.xpath('.//div[@class="Community-item-active blog"]/a/span/text()')
        href = t.xpath('.//div[@class="Community-item-active blog"]/a/@href')
        try:
            print(name[0], href[0])
        except:
            pass



for i in range(2, 4):
    web.find_element_by_xpath('//*[@id="floor-blog-nav_746"]/div/div[2]/a[{}]'.format(i)).click()
    time.sleep(1)
    for t in range(5):
        js = "var q=document.documentElement.scrollTop=" + str(t * 1000)
        web.execute_script(js)
        time.sleep(3)
    html = web.page_source
    get_page(html)
    time.sleep(2)
    print('----------------------------------')
