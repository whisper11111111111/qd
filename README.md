# 签到
通过扫描二维码，即可跳转到签到页面，填入的信息可自动保存到user_data.xlsx中
## 使用方法
安装ngrok

`<ngrok http 5000>`

修改index.html中的

`<<script>
        var baseUrl = " 新的ngrok映射外网的域名";>`

运行app.py
