"""
@Project（项目）: None
@Author（作者）: 刘星宇
@Data（时间）: 2022/03/20
@License:   None
"""
import pytest


class TestLogin:
    data = ["基本版", "English", "手机版", "企业邮箱"]

    @pytest.mark.parametrize("logins", data, indirect=True)         # 传参
    def test_login_language(self, logins):
        """ 切换方式 """
        driver, ls = logins
        driver.header(ls)
        # /html/body/div/div[1]/div/a[4]
