# coding=gb2312
import requests
import json
from Util.EmailUtil import EmailUtil
import sys


def getJson():
    url = "https://api.btc126.com/eth.php"
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    dataarr = json.loads(response.text)
    return dataarr


def wxPush(text: str, desp: str, send: str):
    url = "https://sc.ftqq.com/%s.send" % send
    data = {"text":text , "desp":desp}
    print(url)
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
    con = "���ETH��ǰ�۸�%sUSDT,ԼΪ%sRMB" % (huoBi, rmb)
    userInfoStr = argv[1]
    from_addr = argv[2]  # �ʼ������˺�
    qqCode = argv[3]  # ��Ȩ�루���Ҫ���Լ���ȡ���ģ�
    userInfo = userInfoStr.split("|")
    for user in userInfo:
        email = getValue(user, "email")
        send = getValue(user, "send")
        rmblow = float(getValue(user, "rmblow"))
        rmbhigh = float(getValue(user, "rmbhigh"))
        usdtlow = float(getValue(user, "usdtlow"))
        usdthigt = float(getValue(user, "usdthigt"))
        if rmbhigh != 0 and rmb > rmbhigh:
            s = "<p><div style='color:#F00'>ETH��ǰ�۸��Ѿ�����%sRMB,��ע��Ͷ�ʷ���</div></p>" % rmbhigh
            con = "%s%s" % (con, s)
        if rmblow != 0 and rmb < rmblow:
            s = "<p><div style='color:#00F'>ETH��ǰ�۸��Ѿ�����%sRMB,��ע��Ͷ�ʷ���</div></p>" % rmblow
            con = "%s%s" % (con, s)
        if usdthigt != 0 and huoBi > usdthigt:
            s = "<p><div style='color:#F00'>ETH��ǰ�۸��Ѿ�����%sUSDT,��ע��Ͷ�ʷ���</div></p>" % usdthigt
            con = "%s%s" % (con, s)
        if usdtlow != 0 and huoBi < usdtlow:
            s = "<p><div style='color:#00F'>ETH��ǰ�۸��Ѿ�����%sUSDT,��ע��Ͷ�ʷ���</div></p>" % usdtlow
            con = "%s%s" % (con, s)
        print(con)
        content = "<span>%s</span>" % con
        title = "ETH��ǰ�۸�%sUSDT(��%.2f)" % (huoBi, rmb)
        if len(email) > 0:
            EmailUtil.sendEmail(email, title, content, from_addr, qqCode)
        if len(send) > 0:
            reTest = wxPush(title, content, send)
            print(reTest)


tixing(sys.argv)
