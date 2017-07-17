#coding=utf-8

import HTMLTestRunner
from selenium import webdriver
import unittest, time, re

class Report(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "http://qw.researchreport.cn/report-search"
        self.verificationErrors = []
        self.accept_next_alert = True

    #检查研报列表页数据
    def test_yanbao_page(self):
        """"检查研报列表页数据"""
        driver = self.driver
        driver.get(self.base_url)
        driver.maximize_window()
        time.sleep(1)
        t =driver.find_element_by_xpath(".//*[@id='JS-resultcount']")
        # t =driver.find_element_by_id("JS-resultcount")
        yanbao = t.text
        print "yanbao=",yanbao[0:7]
        shuliang =yanbao[0:7]
        try:
            self.assertEqual(u'找到相关研报约',shuliang)
            print "找到相关研报"
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        time.sleep(2)
        driver.close()

    #检查搜索结果
    def test_yanbao_search(self):
        """检查搜索结果"""
        driver =self.driver
        driver.get(self.base_url)
        driver.maximize_window()
        time.sleep(1)
        driver.find_element_by_xpath(".//*[@id='JS-searchInput']").send_keys(u"平安银行")
        driver.find_element_by_xpath(".//*[@id='JS-searchBtn']").click()
        time.sleep(5)
        title =driver.find_element_by_xpath(".//*[@id='JS-resultlist']/li[1]/div[1]/a")
        gettitle = title.text
        print gettitle

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()

