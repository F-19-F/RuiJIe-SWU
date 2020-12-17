import requests
import re
import urllib.parse
#用户名
username=''
#密码
passwd=''
#是否用手机的Agent，根据需要修改
mobile=False
service='默认'
#可以根据需要修改认证地址，不修改也可以
host='222.198.127.170'




#二重编码
def Quote2(source):
    source=urllib.parse.quote(source,safe='')
    source=urllib.parse.quote(source,safe='')
    return source

#生成Post认证的数据
def GenData(queryString,username=username,password=passwd,service=service):
    data={
        "userId":username,
        "password":password,
        "service":Quote2(service),
        "queryString":Quote2(queryString),
        "operatorPwd":'',
        "operatorUserId":'',
        "validcode":''
    }
    result=''
    i=0
    for item in data:
        i+=1
        result=result+item+'='+data[item]
        if i<len(data):
            result=result+'&'
    return result
#设置请求头部
header={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9"
}
def main():
    if mobile:
        print("模拟手机认证")
        header['User-Agent']="Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36"
    else:
        print("模拟电脑认证")
    global host
    #测试访问，如果不能访问外网，则登录
    res=requests.get(url='http://{}/'.format(host),headers=header)
    try:
        #匹配要跳转的网页
        loginurl=re.findall("'(.*)'",res.text)[0]
        #匹配主机
        host=re.findall('://(.*?)/',loginurl)[0]
        #请求跳转后的网页
    except:
        print("可能已经登陆了呢!")
        return 0
    res=requests.get(url=loginurl,headers=header)
    #根据跳转网页返回的cookies来创建会话
    session=requests.session()
    #根据抓包内容合成cookies
    cookies=requests.utils.dict_from_cookiejar(res.cookies)
    cookies['EPORTAL_COOKIE_OPERATORPWD']=''#根据抓包内容添加
    #根据新的cookies创建会话
    session.cookies = requests.utils.cookiejar_from_dict(cookies, cookiejar=None, overwrite=True)
    header['Content-Type']='application/x-www-form-urlencoded; charset=UTF-8'#Post请求的head需要添加Content-Type才会认证成功
    data=GenData(re.findall('\?(.*)',loginurl)[0])
    try:
        res=session.post(url='http://{}/eportal/InterFace.do?method=login'.format(host),headers=header,data=data)
        loginresult=res.json()
    except:
        print("请确保已经填好密码了，或者是锐捷认证")
        return 0
    ms=loginresult['message']
    if loginresult['result'] == 'success':
        print("登录成功")
    else:
        print("登录失败，原因是:{}".format(ms.encode("raw_unicode_escape").decode("utf-8")))
    return 0
if __name__ == '__main__':
    try:
        main()
    except:
        print("请确认网络是否通畅？")
        exit(-1)