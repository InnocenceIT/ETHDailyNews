# coding=gb2312
import requests
import json
from Util.EmailUtil import EmailUtil
import sys


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

def wxPush(text:str, desp:str, send:str):
    headers = {
        "Cookie": "_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJThmYjJhNTAyNzU0NDZiNDE0ZThhMTE1MDQ3MGNhOTg2BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMVlDM1ozblgrdDl2TEZuWHZlano5NjJRdno4TjlaV0c1eXhOSXZ1Vnl1aWM9BjsARg%3D%3D--9b02012af1e6535418e69003d1300a82fc99a6e5; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1564276936,1564796034,1564796040; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1564796172",
        "If-None-Match": "W/\"9ed3b7f16675401490c68729be9cb96c\"",
        "Host": "www.xicidaili.com",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36"
    }
    url = "http://sc.ftqq.com/%s.send?text=%s&desp=%s" % (send, text, desp)
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    data = json.loads(response.text)
    return data

def getbuy(key: str, dataarr: list):
    for data in dataarr:
        if data["from"] == key:
            return data["buy"]
    return 0


def getValue(s:str, key:str):
    arr = s.split(",")
    for temp in arr:
        temparr = temp.split(":")
        tempkey = temparr[0]
        tempvalue = temparr[0]
        if key == tempkey:
            return tempvalue
    return ""


def tixing(argv):
    dataarr = getJson()

    # keys=["BTER", "ZB", "MXC", "BITFINEX", "OKCOIN", "HUOBI", "BINANCE"]
    usdt = getbuy("USDT", dataarr)
    huobi = getbuy("HUOBI", dataarr)
    rmb = huobi*usdt
    print(usdt)
    con = "火币ETH当前价格：%sUSDT,约为%sRMB" % (huobi, rmb)
    userInfoStr = argv[0]
    print(userInfoStr)
    userInfo = userInfoStr.split("|")
    for user in userInfo:

        email = getValue(user, "email")
        send = getValue(user, "send")
        rmblow = getValue(user, "rmblow")
        rmbhigh = getValue(user, "rmbhigh")
        usdtlow = getValue(user, "usdtlow")
        usdthigt = getValue(user, "usdthigt")
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
        title = "ETH价格提醒"
        if (len(email) > 0):
            EmailUtil.sendEmail(email, title, content)
        if(len(send) > 0):
            wxPush(title, content, send)


tixing(sys.argv)
