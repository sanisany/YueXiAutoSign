import datetime
import requests
from bs4 import BeautifulSoup


def get_now():
    return datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")


class YueXiAutoSign:
    # 登录界面 (提取loginHash)
    _login_page = "https://bbs.wcccc.cc/member.php"  # GET
    # 登录地址
    _login_url = "https://bbs.wcccc.cc/member.php"  # POST
    # 签到地址
    _sign_url = "https://bbs.wcccc.cc/plugin.php"  # GET

    _login_form_data = {"referer": "https://bbs.wcccc.cc/./", "questionid": 0, "answer": ""}

    _login_params = {"mod": "logging","action": "login","loginsubmit": "yes","inajax": 1}

    _login_header = {
        "user=agent": "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35",
        "origin": "https://bbs.wcccc.cc",
        "referer": "https://bbs.wcccc.cc/member.php?mod=logging&action=login",
    }

    _sign_header = {
        "user=agent": "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35",
        "refer": "https://bbs.wcccc.cc/"
    }

    def __init__(self, username, password, is_email=False):
        self._session = requests.session()
        self._username = username
        self._password = password
        self._login_form_data["username"] = username
        self._login_form_data["password"] = password
        if is_email:
            self._login_form_data["loginfield"] = "email"
        else:
            self._login_form_data["loginfield"] = "username"
        self.message = f"月曦论坛签到\n账号:{username}\n"

    def _pick_login_hash(self):
        html = self._session.get(url=self._login_page, params={"mod": "logging", "action": "login"}).text
        soup = BeautifulSoup(html, 'html.parser')
        form_tag = soup.find("form", {"name": "login"})
        login_form_hash = form_tag.find("input", {"name": "formhash", "type": "hidden"}).get("value")
        login_hash_value = form_tag.get("action").split("&")[-1].split("=")[-1]
        return login_form_hash, login_hash_value

    def login(self):
        hashes = self._pick_login_hash()
        self._login_form_data["formhash"] = hashes[0]
        self._login_params["loginhash"] = hashes[1]
        self._login_header["cookie"] = self._solve_cookie()
        login_response = self._session.post(self._login_url, params=self._login_params, data=self._login_form_data,
                                            headers=self._login_header).text
        if "欢迎您回来" in login_response:
            return True
        return False

    def _get_sign_hash(self):
        self._sign_header["cookie"] = self._solve_cookie()
        html = self._session.get(url=self._sign_url, params={"id": "gsignin:index"}, headers=self._sign_header).text
        soup = BeautifulSoup(html, 'html.parser')
        form_tag = soup.find("form", {"id": "scbar_form"})
        sign_form_hash = form_tag.find("input", {"name": "formhash", "type": "hidden"}).get("value")
        return sign_form_hash

    def sign(self):
        sign_hash = self._get_sign_hash()
        self._sign_header["cookie"] = self._solve_cookie()
        response = self._session.get(url=self._sign_url, headers=self._sign_header,
                                     params={"id": "gsignin:index", "action": "signin", "formhash": sign_hash}).text
        if "签到成功" in response:
            return 1
        elif "您今天已经签过到了" in response:
            return 0
        else:
            return -1

    def _solve_cookie(self):
        cookies = self._session.cookies.get_dict()
        cookies_str_list = [f"{k}={v}" for k, v in cookies.items()]
        cookies_str = "; ".join(cookies_str_list)
        return cookies_str

    def start(self):
        login_status = self.login()
        if not login_status:
            self.message += f"{get_now()}\n状态:登录失败\n"
            print(self.message)
            return
        sign_status = self.sign()
        if sign_status == 0:
            self.message += f"{get_now()}\n状态:今日已经签到\n"
        elif sign_status == 1:
            self.message += f"{get_now()}\n状态:签到成功\n"
        else:
            self.message += f"{get_now()}\n状态:签到失败\n"
        self.message += "-----------------\npowered by lolita"
        print(self.message)


if __name__ == "__main__":
    YueXiAutoSign("用户名", "密码", is_email=True).start()
