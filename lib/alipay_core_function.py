#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015    liukelin
#
# @author: iiukelin      314566990@qq.com
# 
#  * 支付宝接口公用函数
#  * 详细：该类是请求、通知返回两个文件所调用的公用函数核心处理文件
#  * 说明：
#  * 以下代码只是为了方便商户测试而提供的样例代码，商户可以根据自己网站的需要，按照技术文档编写,并非一定要使用该代码。
#  * 该代码仅供学习和研究支付宝接口使用，只是提供一个参考。
 
# import ujson as json
import time
import urllib
import StringIO
import pycurl

#urlencode 
def my_urlencode(str) :
    reprStr = repr(str).replace(r'\x', '%')
    return reprStr[1:-1]

# 
#  把数组所有元素，按照“参数=参数值”的模式用“&”字符拼接成字符串
#  @param para 需要拼接的字典
#  @param keys 字典key排序数组
#  return 拼接完成以后的字符串
#  
def createLinkstring(para, keys=[]) :

    # print "para:%s,keys:%s" %(para, keys)
    arg = ""
    if len(keys)>0:
        for k in keys:
            arg += "%s=%s&" %(str(k), str(para[k]))
    else :
        for i in para :
            arg += "%s=%s&" %(str(i), str(para[i]))

    #如果存在转义字符，那么去掉转义
    #去掉最后一个&字符
    return arg[:-1]

# 
#  把数组所有元素，按照“参数=参数值”的模式用“&”字符拼接成字符串，并对字符串做urlencode编码
#  @param para 需要拼接的字典
#  @param keys 字典key排序数组
#  return 拼接完成以后的字符串
#  
def createLinkstringUrlencode(para,keys = []) :
    arg = ""
    if len(keys)>0:
        for k in keys:
             arg += "%s=%s&" %(k, my_urlencode(para[k]))
    else :
        for i in para :
            arg += "%s=%s&" %(i, my_urlencode(para[i]))
    #如果存在转义字符，那么去掉转义
    #去掉最后一个&字符
    return arg[:-1]

# 
#  除去数组中的空值和签名参数
#  @param $para 签名参数组
#  return 去掉空值与签名参数后的新签名参数组
# 
def paraFilter(para) :
    para_filter = {}
    for key in para :
        if key=="sign" or key == "sign_type" or para[key] == "" or para[key] == "key":
            continue
        para_filter[key] = para[key]
    return para_filter

# 
#  对字典按键排序 (因为python字典是无序的 需自行按key取得)
#  @param para 排序前的字典
#  return 排序后的key数组 
# 
def argSort(para) :
    # print "====para:%s===" % para
    # para = sorted(para.iteritems(), key=lambda d:d[0]) # 对字典按键（key）排序
    # newpara = {}
    # for k in para:
    #     newpara[k[0]] = k[1]
    keys = para.keys()
    keys.sort()
    return keys

""""
 * 写日志，方便测试（看网站需求，也可以改成把记录存入数据库）
 * 注意：服务器需要开通fopen配置
 * @param $word 要写入日志里的文本内容 默认值：空值
 """
def logResult(word='') :
    file_object = open('log.txt', 'a')
    time_ = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    file_object.write(" 执行日期:\n %s \n" %(time_, word))
    file_object.close( )


"""
 * 远程获取数据，POST模式 (这里就用request算了)
 * 注意：
 * 1.使用Crul需要修改服务器中php.ini文件的设置，找到php_curl.dll去掉前面的";"就行了
 * 2.文件夹中cacert.pem是SSL证书请保证其路径有效，目前默认路径是：getcwd().'\\cacert.pem'
 * @param $url 指定URL完整路径地址
 * @param $cacert_url 指定当前工作目录绝对路径
 * @param $para 请求的数据
 * @param $input_charset 编码格式。默认值：空值
 * return 远程输出的数据
 """
def getHttpResponsePOST(url, cacert_url, para, input_charset = '') :
    # import pycurl
    if input_charset.lstrip() != '':
        url = "%s_input_charset=%s" %(url,  input_charset )
    # responseText = requests.post( url, data=para)
    curl = pycurl.Curl()
    f = StringIO.StringIO()
    curl.setopt(curl.URL, url)
    curl.setopt(curl.WRITEFUNCTION, f.write)
    curl.setopt(pycurl.SSL_VERIFYPEER, 1)   #SSL证书认证
    curl.setopt(pycurl.SSL_VERIFYHOST, 2)  #严格认证
    curl.setopt(pycurl.CAINFO, cacert_url) #证书地址
    # curl.setopt(pycurl.SSLCERTTYPE, "PEM")  
    # curl.setopt(pycurl.SSLCERT, '/home/youmi/Desktop/sys/wap_alipay/alipay_batch_trans/cacert.pem')
    curl.setopt(curl.HEADER, 0)  # CURLOPT_HEADER
    # curl.setopt(pycurl.CURLOPT_HTTPPOST, 1)  # post传输数据
    curl.setopt(curl.POSTFIELDS, urllib.urlencode(para))  # post传输数据
    # curl.setopt(pycurl.HEADERFUNCTION, headerCookie)
    # curl.setopt(pycurl.COOKIE,Cookie)
    curl.perform()
    responseText = ''
    if curl.getinfo(pycurl.RESPONSE_CODE) == 200:
        responseText = f.getvalue()
    curl.close()
    f.close()
    return responseText

"""
 * 远程获取数据，GET模式 (这里就用request算了)
 * 注意：
 * 1.使用Crul需要修改服务器中php.ini文件的设置，找到php_curl.dll去掉前面的";"就行了
 * 2.文件夹中cacert.pem是SSL证书请保证其路径有效，目前默认路径是：getcwd().'\\cacert.pem'
 * @param $url 指定URL完整路径地址
 * @param $cacert_url 指定当前工作目录绝对路径
 * return 远程输出的数据
 """
def  getHttpResponseGET(url, cacert_url ) :
    import requests
    r = requests.get(url)
    responseText = r.text
    '''
    curl = pycurl.Curl()
    f = StringIO.StringIO()
    curl.setopt(curl.URL, url)
    curl.setopt(curl.WRITEFUNCTION, f.write)
    curl.setopt(pycurl.SSL_VERIFYPEER, 1)   #SSL证书认证
    curl.setopt(pycurl.SSL_VERIFYHOST, 2)  #严格认证
    curl.setopt(pycurl.CAINFO, cacert_url) #证书地址
    # curl.setopt(pycurl.SSLCERTTYPE, "PEM")  
    # curl.setopt(pycurl.SSLCERT, '/home/youmi/Desktop/sys/wap_alipay/alipay_batch_trans/cacert.pem')
    curl.setopt(curl.HEADER, 0)  # CURLOPT_HEADER
    # curl.setopt(pycurl.CURLOPT_HTTPPOST, 1)  # post传输数据
    # curl.setopt(curl.POSTFIELDS, urllib.urlencode(para))  # post传输数据
    # curl.setopt(pycurl.HEADERFUNCTION, headerCookie)
    # curl.setopt(pycurl.COOKIE,Cookie)
    curl.perform()
    responseText = f.getvalue()
    curl.close()
    f.close()
    '''
    return responseText

""""
 * 实现多种字符编码方式
 * @param $input 需要编码的字符串
 * @param $_output_charset 输出的编码格式
 * @param $_input_charset 输入的编码格式
 * return 编码后的字符串
 """
def charsetEncode( input, _output_charset , _input_charset):
    output = ""
    if not _output_charset :
        _output_charset = _input_charset

    if (_input_charset == _output_charset) or not input :
        output = input
    else :
        output = input.encode(_output_charset)
        # die "sorry, you have no libs support for charset change."
    return output