# coding=utf-8
import requests
import json
from Util.EmailUtil import EmailUtil
import sys


def getJson():
    url = "https://eth.btc126.com/eth.php"
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    dataarr = json.loads(response.text)
    return dataarr


def wxPush(text: str, desp: str, send: str):
    url = "https://sc.ftqq.com/%s.send" % send
    data = {"text": text, "desp": desp}
    response = requests.post(url, data)
    response.encoding = response.apparent_encoding
    return response.text


def getBuy(key: str, dataArr: list):
    for data in dataArr:
        if data["from"] == key:
            return data["buy"]
    return 0


def getValue(s: str, key: str):
    arr = s.split(",")
    for temp in arr:
        temparr = temp.split(":")
        tempkey = temparr[0]
        tempvalue = temparr[1]
        if key == tempkey:
            return tempvalue
    return ""


def tixing(argv):
    dataArr = getJson()
    # keys=["BTER", "ZB", "MXC", "BITFINEX", "OKCOIN", "HUOBI", "BINANCE"]
    usdt = getBuy("USDT", dataArr)
    huoBi = getBuy("HUOBI", dataArr)
    rmb = huoBi*usdt
    con = "火币ETH当前价格：%sUSDT,约为%.2fRMB" % (huoBi, rmb)
    userInfoStr = argv[1]
    from_addr = argv[2]  # 邮件发送账号
    qqCode = argv[3]  # 授权码（这个要填自己获取到的）
    userInfo = userInfoStr.split("|")
    for user in userInfo:
        email = getValue(user, "email")
        send = getValue(user, "send")
        rmblow = float(getValue(user, "rmblow"))
        rmbhigh = float(getValue(user, "rmbhigh"))
        usdtlow = float(getValue(user, "usdtlow"))
        usdthigt = float(getValue(user, "usdthigt"))
        if rmbhigh != 0 and rmb > rmbhigh:
            s = "<p><div style='color:#F00'>ETH当前价格已经超过%sRMB,请注意投资风险</div></p>" % rmbhigh
            con = "%s%s" % (con, s)
        if rmblow != 0 and rmb < rmblow:
            s = "<p><div style='color:#00F'>ETH当前价格已经低于%sRMB,请注意投资风险</div></p>" % rmblow
            con = "%s%s" % (con, s)
        if usdthigt != 0 and huoBi > usdthigt:
            s = "<p><div style='color:#F00'>ETH当前价格已经超过%sUSDT,请注意投资风险</div></p>" % usdthigt
            con = "%s%s" % (con, s)
        if usdtlow != 0 and huoBi < usdtlow:
            s = "<p><div style='color:#00F'>ETH当前价格已经低于%sUSDT,请注意投资风险</div></p>" % usdtlow
            con = "%s%s" % (con, s)
        content = "<span>%s</span>" % con
        title = "ETH当前价格%sUSDT约%.2f人民币" % (huoBi, rmb)
        if len(email) > 0:
            EmailUtil.sendEmail(email, title, content, from_addr, qqCode)
        if len(send) > 0:
            reTest = wxPush(title, content, send)
            print(reTest)


tixing(sys.argv)
