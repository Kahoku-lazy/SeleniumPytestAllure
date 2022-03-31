"""
@Project（项目）: None
@Author（作者）: 刘星宇
@Data（时间）: 2022/03/20
@License:   None
"""
from base.box import SeleniumCommon


class BasePage(object):

    def __init__(self):
        """ 实例化 """
        self.driver = SeleniumCommon()

    def open_url(self, url):
        """ 打开网站 """
        self.driver.navigate(url)

    def click(self, selector):
        """ 点击 """
        self.driver.explicitly_wait(selector, 10)
        self.driver.click(selector)

    def input_text(self, selector, text):
        """ 文本框输入 """
        self.driver.explicitly_wait(selector, 10)
        self.driver.type(selector, text)

    def save_img(self, file_name):
        """ 截图 """
        self.driver.save_window_snapshot(file_name)