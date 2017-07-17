#coding=utf-8

import HTMLTestRunner
from selenium import webdriver
import unittest, time, re

class Notice(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "http://qw.researchreport.cn/notice/new-notice"
        self.verificationErrors = []
        self.accept_next_alert = True

    # 检查研报列表页数据
    def test_gonggao_page(self):
        """"检查研报列表页数据"""
        driver = self.driver
        driver.get(self.base_url)
        driver.maximize_window()
        time.sleep(1)
        t = driver.find_element_by_xpath(".//*[@id='JS-resultcount']")
        # t =driver.find_element_by_id("JS-resultcount")
        yanbao = t.text
        print "yanbao=", yanbao[0:6]
        shuliang = yanbao[0:6]
        try:
            self.assertEqual(u'找到相关公告', shuliang)
            print "找到相关公告"
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        time.sleep(2)
        driver.close()

    #检查公告列表页数据是否是今天的
    def test_gonggao_search(self):
        """检查公告列表页数据是否是今天的"""
        driver =self.driver
        driver.get(self.base_url)
        driver.maximize_window()
        time.sleep(3)
        data =driver.find_element_by_xpath(".//*[@id='JS-resultlist']/li[1]/div[2]/div/span[2]")
        time.sleep(1)
        publish_at = data.text
        print publish_at
        try:
            self.assertEqual(u"今天",publish_at)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        time.sleep(2)
        driver.close()

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()

