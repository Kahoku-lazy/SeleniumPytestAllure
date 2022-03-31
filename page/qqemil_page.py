"""
@Project（项目）: None
@Author（作者）: 刘星宇
@Data（时间）: 2022/03/20
@License:   None
"""
import pytest

from page.base_page import BasePage

@pytest.mark.parametrize
class QqEmilPage(BasePage):

    def header(self, header):
        """ 切换 标题 """
        index = None
        if header == "基本版":
            index = 1
        elif header == "English":
            index = 2
        elif header == "手机版":
            index = 3
        elif header == "企业邮箱":
            index = 4

        if index is not None:
            self.click('x, /html/body/div/div[1]/div/a[%d]' % index)    #/html/body/div/div[1]/div/a[4]
        else:
            raise "无法找到此标题{index}".format(index=index)