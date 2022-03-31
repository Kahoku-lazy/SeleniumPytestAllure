"""
@Project（项目）: box
@Author（作者）: 刘星宇
@Data（时间）: 2022/03/14
@License:   None
"""

import time
from enum import Enum, unique
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select

''' 公共方法 '''


@unique
class BrowserDriver(Enum):
    """ 定义支持的浏览器，支持Chrome、Firefox、Ie、Edge """

    Chrome = 0
    Firefox = 1
    Ie = 2
    Edge = 3


class SeleniumCommon(object):
    """封装 selenium 工具中的方法 """
    _base_driver = None
    _browser_driver_path = None

    def __init__(self, brower_type=0, by_char=",") -> None:
        """
        构造方法
        :param brower_type: 枚举浏览器参数
        :param by_char: 间隔符（用于定位元素）
        """

        driver = None
        self._by_char = by_char  # 定位元素分隔符
        # 选择浏览器
        if brower_type == 0 or brower_type == BrowserDriver.Chrome:
            driver = webdriver.Chrome()
        elif brower_type == 1 or brower_type == BrowserDriver.Firefox:
            driver = webdriver.Firefox()
        elif brower_type == 2 or brower_type == BrowserDriver.Ie:
            driver = webdriver.Ie()
        elif brower_type == 3 or brower_type == BrowserDriver.Edge:
            driver = webdriver.Edge()

        # 浏览器未打开时，抛出异常
        try:
            self._base_driver = driver
        except Exception:
            raise NameError("浏览器{name}打开失败！！！".format(name=brower_type))

    '''  将自定义的selector转化为(By.ID, value)格式 '''

    def _concert_selector_to_locatot(self, selector):
        """
        自定义定位元素格式, 并将其转化为Selenium 支持的 (By.ID, value)格式
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :return: None
        """

        if self._by_char not in selector:  # 定位元素无标志符，默认为ID定位方式
            return By.ID, selector

        # 拆分"i, xxx"
        selector_by = selector.split(self._by_char)[0].strip()
        selector_value = selector.split(self._by_char)[1].strip()

        # 定位方法匹配
        if selector_by == "i" or selector_by == "id":
            locator = (By.ID, selector_value)
        elif selector_by == "n" or selector_by == "name":
            locator = (By.NAME, selector_value)
        elif selector_by == "c" or selector_by == "class_name":
            locator = (By.CLASS_NAME, selector_value)
        elif selector_by == "l" or selector_by == "link_text":
            locator = (By.LINK_TEXT, selector_value)
        elif selector_by == "p" or selector_by == "partial_link_text":
            locator = (By.PARTIAL_LINK_TEXT, selector_value)
        elif selector_by == "t" or selector_by == "tag_name":
            locator = (By.TAG_NAME, selector_value)
        elif selector_by == "x" or selector_by == "xpath":
            locator = (By.XPATH, selector_value)
        elif selector_by == "s" or selector_by == "css_selector":
            locator = (By.CSS_SELECTOR, selector_value)
        else:
            raise NameError("Please enter a valid selector of targeting elements.")

        return locator

    def _locator_element(self, selector):
        """
        选择单个元素
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :return: None
        """
        locator = self._concert_selector_to_locatot(selector)

        if locator is not None:
            return self._base_driver.find_element(*locator)
        else:
            raise NameError("请按格式输入有效的定位元素。")

    def _locator_elements(self, selector):
        """
        选择复数元素
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :return: None
        """

        locator = self._concert_selector_to_locatot(selector)

        if locator is not None:
            return self._base_driver.find_elements(*locator)
        else:
            raise NameError("请按格式输入有效的定位元素。")

    ''' 浏览器控制 '''

    def navigate(self, url):
        """
        打开网站
        :param url: 网站地址
        :return: None
        """
        self._base_driver.get(url)

    def maximize_windows(self):
        """
        窗口最大化
        :return: None
        """

        self._base_driver.maximize_window()

    def minximize_windows(self):
        """
        窗口最小化
        :return: None
        """

        """ 最小化窗口 """
        self._base_driver.minimize_window()

    def refresh(self, url=None):
        """
        刷新页面
        :param url: 页面网址
        :return: None
        """

        if url is None:
            self._base_driver.refresh()
        else:
            self._base_driver.get(url)

    def button_back(self):
        """
        浏览器 后退
        :return: None
        """

        self._base_driver.back()

    def button_forward(self):
        """
        浏览器 前进
        :return: None
        """

        self._base_driver.forward()

    def close_browser(self):
        """
        关闭窗口或者标签页
        :return: None
        """

        self._base_driver.close()

    def quit_driver(self):
        """
        退出 浏览器驱动
        :return: None
        """

        self._base_driver.quit()

    ''' 浏览器页面元素相关操作方法 '''

    def click(self, selector):
        """
        鼠标点击（默认左键）
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :return: None
        """

        self._locator_element(selector).click()

    def type(self, selector, value):
        """
        选定输入框  输入文本
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :param value: 输入内容
        :return: None
        """

        el = self._locator_element(selector)
        el.clear()
        el.send_keys(value)

    """ 复选框、下拉框操作 """

    def select_by_index(self, selector, index):
        """
        index的方式 点击选择复选框，单选按钮，甚至下拉框
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :param index: 标签 下标值（int number）
        :return: None
        """

        el = self._locator_element(selector)
        Select(el).select_by_index(index)

    """ 获取数据 """

    def get_url(self):
        """
        获取当前页面的URL
        :return:  url (string)
        """

        return self._base_driver.current_url

    def get_title(self):
        """
        获取当前页面的标题
        :return:  页面窗口标题
        """

        return self._base_driver.title

    def get_handle(self):
        """
        获取当前窗口的窗口句柄
        :return:
        """

        return self._base_driver.current_window_handle

    def get_selected(self, selector):
        """
        返回一个元素的选定状态, (适用于 单选框 复选框)
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :return: True False
        """
        el = self._locator_element(selector)
        return el.is_selected()

    """ 判断页面元素"""

    def get_exist(self, selector):
        """
        该方法用来确认元素是否存在，如果存在返回flag=true，否则返回false
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :return: None
        """

        flag = True
        try:
            self._locator_element(selector)
            return flag
        except:
            flag = False
            return flag

    def get_enabled(self, selector):
        """
        判断页面元素是否可点击
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :return: 布尔值 (bool)
        """

        if self._locator_element(selector).is_enabled():
            return True
        else:
            return False

    def get_displayed(self, selector):
        """
        获取要显示的元素，返回的结果为真或假
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        Usage:
        driver.get_display("i,el")
        :return:
        """
        el = self._locator_element(selector)
        return el.is_displayed()

    """ web页面alert警告框 相关处理方法 """

    def accept_alert(self):
        """
        接受 Alert 警告框
        :return: None
        """

        self._base_driver.switch_to.alert.accept()

    def dismiss_alert(self):
        """
        取消 Alert 警告框
        :return: None
        """

        self._base_driver.switch_to.alert.dismiss()

    def get_alert_text(self):
        """
        获取 Alert弹框的文本内容
        :return: None
        """
        text = self._base_driver.switch_to.alert.text
        return text

    """  等待方法 """

    def forced_wait(self, seconds):
        """  强制等待
        :param seconds: 秒 （s）
        :return: None
        """
        time.sleep(seconds)

    def implicitly_wait(self, seconds):
        """
        隐式等待
        :param seconds: 秒 (s)
        """
        self._base_driver.implicitly_wait(seconds)

    def explicitly_wait(self, selector, seconds):
        """
        显式等待（等待某一元素出现的最大时间）
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :param seconds: 最长等待时间，秒 （s）
        :return: None
        """
        locator = self._concert_selector_to_locatot(selector)

        WebDriverWait(self._base_driver, seconds).until(expected_conditions.presence_of_element_located(locator))

    """ 浏览器标签窗口 相关处理方法 """

    def switch_to_frame(self, selector):
        """
        进入 iframe 框架
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :return:
        """

        el = self._locator_element(selector)
        self._base_driver.switch_to.frame(el)

    """ 屏幕截图 相关方法"""

    def save_window_snapshot(self, file_name):
        """
        屏幕截图
        :param file_name: 截图保存的路径
        :return: None
        """

        driver = self._base_driver
        driver.save_screenshot(file_name)
