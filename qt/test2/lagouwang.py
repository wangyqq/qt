from selenium import webdriver
import requests
from lxml import etree
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import re
import random  # 随机模块
import json
proxy = '113.241.138.194:4210'

def login(driver):
    with open('cookies2.txt', 'r', encoding='utf8') as f:
        cookies = json.loads(f.read())
    # 给浏览器添加cookies
    for cookie in cookies:
        cookie_dict = {
            'domain': '.lagou.com',
            'name': cookie.get('name'),
            'value': cookie.get('value'),
            "expiry": 1706353356,
            'path': '/',
            'httpOnly': False,
            'Secure': False,
        }
        # print(cookie_dict)
        driver.add_cookie(cookie_dict)
    # 刷新网页，cookies才会成功
    driver.refresh()

class lagouSpitder(object):
    option = webdriver.ChromeOptions()
    # option.add_argument('--headless')
    option.add_argument('--proxy-server=http://' + proxy)
    option.add_experimental_option('useAutomationExtension', False)
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver_path = r'D:\迅雷下载\chromedriver.exe'  # 定义好路径

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=lagouSpitder.driver_path,
                                       options=lagouSpitder.option)  # 初始化路径+规避检测selenium框架
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
        })
        self.url = 'https://www.lagou.com/jobs/list_python/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput='
        self.positions = []

    def run(self):  # 主页面
        self.driver.get(self.url)  # 去请求主页面
        login(self.driver)
        time.sleep(3)
        while True:
            source = self.driver.page_source  # source页面来源  先获取一页
            WebDriverWait(driver=self.driver, timeout=10).until(
                EC.presence_of_element_located((By.XPATH, '//span[@action="next"]'))
            )  # 等待按钮加载出来，避免没加载出来就点击导致的报错
            self.parse_list_page(source)  # 解析完获取的这一页职位之后，去点击下一页
            next_btn = self.driver.find_element_by_xpath('//span[@action="next"]')  # 下一页的元素位置
            if "pager_next pager_next_disabled" in next_btn.get_attribute('class'):  # 如果class等于最后一页则停止，否则继续点击
                break
            else:
                next_btn.click()  # 点击下一页
                time.sleep(1)

    def parse_list_page(self, source):  # 获取职位详情页url
        html = etree.HTML(source)
        links = html.xpath('//a[@class="position_link"]/@href')
        for link in links:  # 循环去解析详情页
            self.request_detall_page(link)
            time.sleep(random.uniform(1, 3))  # 随机暂停

    def request_detall_page(self, url):  # 去请求细节页面
        # self.driver.get(url)
        self.driver.execute_script("window.open('%s')" % url)  # 新打开一个职位页面
        self.driver.switch_to_window(self.driver.window_handles[1])  # 切换到当前页面来解析，不切换的话selenium会停留在上一页
        source = self.driver.page_source  # source页面来源
        self.pares_detail_page(source)  # 解析页面
        self.driver.close()  # 解析完关闭页面
        time.sleep(0.5)
        self.driver.switch_to_window(self.driver.window_handles[0])  # 切换回主页面

    def pares_detail_page(self, source):  # 获取职位细节信息
        html = etree.HTML(source)
        Position_name = html.xpath('//span[@class="position-head-wrap-position-name"]/text()')[0]  # 职位名字
        salary = html.xpath('//span[@class="salary"]/text()')[0]  # 薪水
        Position_the_temptation = html.xpath('//dd[@class="job-advantage"]/p/text()')[0]  # 职位诱惑
        Job_description = html.xpath('//div[@class="job-detail"]//text()')  # 职位详情
        # Job_description=re.sub(r'[\s/]','',Job_description)
        desc = ''.join(html.xpath('//div[@class="job-detail"]//text()')).strip()  # 拼接
        work_address = html.xpath('//div[@class="work_addr"]//text()')[3]  # 工作地址
        CompanyName = html.xpath('//h3[@class="fl"]/em/text()')[0]  # 公司名字
        Company_Basic_Information = html.xpath('//li/h4/text()')  # 公司基本信息

        position = {
            '职位名字': Position_name,
            '薪水': salary,
            '职位诱惑': Position_the_temptation,
            '职位详情': Job_description,
            '工作地址': work_address,
            '公司名字': CompanyName,
            '公司基本信息': Company_Basic_Information,
        }
        self.positions.append(position)
        print(position)
        print('=' * 40)


if __name__ == '__main__':
    spider = lagouSpitder()
    spider.run()
