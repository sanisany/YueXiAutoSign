### 月曦论坛自动签到.Py

#### 免责声明
本文件仅供学习和技术交流使用，不得用于非法用途。对于因滥用而导致的任何法律责任，本人概不负责。

#### 环境要求:
    基于以下包版本编写:
    requests >=2.28.2 
    beautifulsoup4 >= 4.12.2

#### 使用说明
1. 修改YueXiSign.py的最后的 `if__name__=="__main__":` 函数:
替换其中的 `用户名/邮箱` 和 `密码`
```python
if __name__ == "__main__":
    # 用户名-密码登录
    YueXiAutoSign("用户名", "密码").start()
    # 邮箱-密码登录
    YueXiAutoSign("邮箱", "密码", is_email = True).start()
```
    