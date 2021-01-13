# ETHDailyNews
 定时获取当前ETH价格并通过邮件、微信发送提醒
## 设置
  **进入Settings-> Secrets-> New Secrets 添加以下3个Secrets。它们将作为应用启动时的命令行参数被传入程序。** 
 
 FROMADDR   发送邮箱（暂时只能QQ邮箱）
 
 QQCODE     授权码（QQ邮箱获取）
 
 USERINFO   用户信息格式如下
 
 ### USERINFO
 email:接收邮件的邮箱,send:server酱send,rmblow:人民币低价提醒,rmbhigh:人民币高价提醒,usdtlow:USDT低价提醒,usdthigt:USDT高价提醒
 如email:123456@qq.com,send:abcdef,rmblow:10,rmbhigh:0,usdtlow:0,usdthigt:1000
 邮箱和send可不填，价格提醒为0即为不提醒（但还是会推送价格信息）多个账号用|分隔
 
 