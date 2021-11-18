# coding=utf-8
import requests
import json
import datetime
from datetime import date, timedelta
from Util.EmailUtil import EmailUtil
import sys


def getJson(url):
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    data = json.loads(response.text)
    return data


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


def ETH(argv):
    # url = "https://api.btc126.com/eth.php"
    url = "https://eth.btc126.com/eth.php"
    dataArr = getJson(url)
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
def zhaiquan(argv):
    userInfoStr = argv[1]
    from_addr = argv[2]  # 邮件发送账号
    qqCode = argv[3]  # 授权码（这个要填自己获取到的）
    url = "http://datacenter-web.eastmoney.com/api/data/v1/get?sortColumns=PUBLIC_START_DATE&sortTypes=-1&pageSize=20&pageNumber=1&reportName=RPT_BOND_CB_LIST&columns=ALL"
    data = getJson(url)
    dataArr = data["result"]["data"]
    # print(dataArr)
    userInfo = userInfoStr.split("|")
    for user in userInfo:
        email = getValue(user, "email")
        send = getValue(user, "send")
        rpt = getValue(user, "rpt")
        if rpt == "true":
            con = ""
            for data in dataArr:
                print(data["SECURITY_NAME_ABBR"],"\t",data["PUBLIC_START_DATE"],"\t",data["ACTUAL_ISSUE_SCALE"],"\t\t",data["RATING"])
                public_start_date=datetime.datetime.strptime(data["PUBLIC_START_DATE"],"%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
                # tomorrow="2021-09-29"
                if public_start_date==tomorrow:
                    temp="名称：%s----规模：%s（亿元）-----评级：%s"%(data["SECURITY_NAME_ABBR"],data["ACTUAL_ISSUE_SCALE"],data["RATING"])
                    con="%s%s"%(con,temp)
                    # print(con)
            if len(con)==0:
                continue
            content = "<span>%s</span>" % con
            title = "明日有新债申购"
            if len(email) > 0:
                EmailUtil.sendEmail(email, title, content, from_addr, qqCode)
            if len(send) > 0:
                reTest = wxPush(title, content, send)
                # print(reTest)
            
def tixing(argv):
    # ETH(argv)
    zhaiquan(argv)
    
               
tixing(sys.argv)
