"""
@Project（项目）: None
@Author（作者）: 刘星宇
@Data（时间）: 2022/03/20
@License:   None
"""
import pytest
from page.qqemil_page import QqEmilPage

@pytest.fixture(scope="module")
def logins(request):
    """ 测试QQ邮箱登陆 前置条件 """
    param = request.param
    driver = QqEmilPage()
    driver.open_url("https://mail.qq.com/")
    yield driver, param
