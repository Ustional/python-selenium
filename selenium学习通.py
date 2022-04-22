import time
from selenium import webdriver

web = webdriver.Chrome()
web.get(
    'https://mooc2-ans.chaoxing.com/mycourse/stu?courseid=212425681&clazzid=52288576&cpi=161661753&enc'
    '=ccca9ed1d94e8303207d4d888ff6b71d&t=1650282216762&pageHeader=1')
web.maximize_window()
# 登录
web.find_element_by_xpath('//*[@id="phone"]').send_keys('17347593420')
web.find_element_by_xpath('//*[@id="pwd"]').send_keys('sui1756224213...')
web.find_element_by_xpath('//*[@id="loginBtn"]').click()
time.sleep(2)
# 进入第一个知识点
frame_content = web.find_element_by_xpath('//*[@id="frame_content-zj"]')
web.switch_to.frame(frame_content)
table = web.find_elements_by_xpath('//div[@class="catalog_level"]/ul/li')
time.sleep(2)
# if len(web.find_elements_by_xpath('//div[@class="catalog_state icon_yiwanc catalog_tishi56"]')) == len(table):
#     print('所有页面已完成')
# else:
web.find_element_by_xpath('//*[@id="fanyaChapter"]/div/div[2]/div[2]/div[2]/div[2]/ul/li[1]/div/div/div[2]').click()
count = 0
page = 0
page1 = 1
while count < len(table):
    print('page1 = %d' % page1)
    tables = web.find_elements_by_xpath('//*[@id="coursetree"]/ul/li[{}]/div[2]/ul/li'.format(page1))
    print('tables = %d' % len(tables))
    frame1 = web.find_element_by_xpath('//*[@id="iframe"]')  # 进入的第一个iframe
    web.switch_to.frame(frame1)
    frame2 = web.find_element_by_xpath('//*[@id="ext-gen1044"]/iframe')  # 进入第二个iframe
    web.switch_to.frame(frame2)
    time.sleep(3)
    web.find_element_by_xpath('//*[@id="video"]/button').click()  # 点击播放按钮
    time.sleep(2)
    web.find_element_by_xpath('//*[@id="video"]/div[5]/div[6]/button').click()  # 点击静音按钮
    time.sleep(2)
    for i in range(3):
        web.find_element_by_xpath('//*[@id="video"]/div[5]/div[1]/button').click()  # 点击2倍速
    pause_btn = web.find_element_by_xpath('//button[contains(@class,"vjs-play-control")and '
                                          'contains(@class,"vjs-control")and contains(@class,"vjs-button")]')
    bf_btn = web.find_element_by_xpath('//*[@id="video"]/div[5]/button[1]')
    while 1:  # 播放等待
        time.sleep(1)  # 每1秒，检查视频是否播放完毕
        if bf_btn.get_attribute('title') == '播放':
            bf_btn.click()
        if pause_btn.get_attribute('title') == "重播":  # 点击后播放，即播放完毕状态
            break
    print('视频播放完毕')
    # 视频播放完毕，退出播放iframe，然后退出循环.
    web.switch_to.default_content()
    count += 1
    page += 1
    print('page=%d' % page)
    if page == len(tables) + 1:
        page = 1
        page1 += 1
    web.find_element_by_xpath('//*[@id="coursetree"]/ul/li[{}]/div[2]/ul/li[{}]'.format(page1, page)).click()
    time.sleep(2)
