# coding=gb2312
import requests
import json
from Util.EmailUtil import EmailUtil


def getJson():
    headers = {
        "Cookie": "_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJThmYjJhNTAyNzU0NDZiNDE0ZThhMTE1MDQ3MGNhOTg2BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMVlDM1ozblgrdDl2TEZuWHZlano5NjJRdno4TjlaV0c1eXhOSXZ1Vnl1aWM9BjsARg%3D%3D--9b02012af1e6535418e69003d1300a82fc99a6e5; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1564276936,1564796034,1564796040; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1564796172",
        "If-None-Match": "W/\"9ed3b7f16675401490c68729be9cb96c\"",
        "Host": "www.xicidaili.com",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36"
    }
    url = "https://api.btc126.com/eth.php"
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    dataarr = json.loads(response.text)
    return dataarr


def getbuy(key: str, dataarr: list):
    for data in dataarr:
        print(data["from"])
        print(key)
        if data["from"] == key:
            return data["buy"]
    return 0


def tixing():
    dataarr = getJson()

    # keys=["BTER", "ZB", "MXC", "BITFINEX", "OKCOIN", "HUOBI", "BINANCE"]
    usdt = getbuy("USDT", dataarr)
    huobi = getbuy("HUOBI", dataarr)
    rmb = huobi*usdt
    print(usdt)
    con = "火币ETH当前价格：%sUSDT,约为%sRMB" % (huobi, rmb)
    userInfoStr = """[{"email": "825639602@qq.com","rmblow": 1000,"rmbhigh": 0,"usdtlow": 0,"usdthigt": 1300}]"""
    userInfo = json.loads(userInfoStr)
    for user in userInfo:
        email = user["email"]
        rmblow = user["rmblow"]
        rmbhigh = user["rmbhigh"]
        usdtlow = user["usdtlow"]
        usdthigt = user["usdthigt"]
        if rmbhigh != 0 and rmb > rmbhigh:
            s = "<p><div style='color:#F00'>ETH当前价格已经超过%sRMB,请注意投资风险</div></p>" % rmbhigh
            con = "%s%s" % (con, s)
        if rmblow != 0 and rmb < rmblow:
            s = "<p><div style='color:#00F'>ETH当前价格已经低于%sRMB,请注意投资风险</div></p>" % rmblow
            con = "%s%s" % (con, s)
        if usdthigt != 0 and huobi > usdthigt:
            s = "<p><div style='color:#F00'>ETH当前价格已经超过%sUSDT,请注意投资风险</div></p>" % usdthigt
            con = "%s%s" % (con, s)
        if usdtlow != 0 and huobi < usdtlow:
            s = "<p><div style='color:#00F'>ETH当前价格已经低于%sUSDT,请注意投资风险</div></p>" % usdtlow
            con = "%s%s" % (con, s)
        print(con)
        content = "<span>%s</span>" % con
        EmailUtil.sendEmail(email, "ETH价格提醒", content)


tixing()
