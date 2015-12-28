#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015    liukelin
#
# @author: iiukelin      314566990@qq.com
"""
# MD5
# 详细：MD5加密
# 日期：2015-12-25
# 说明：
# 以下代码只是为了方便商户测试而提供的样例代码，商户可以根据自己网站的需要，按照技术文档编写,并非一定要使用该代码。
# 该代码仅供学习和研究支付宝接口使用，只是提供一个参考。
 """

import md5

"""
 * 签名字符串
 * @param $prestr 需要签名的字符串
 * @param $key 私钥
 * return 签名结果
 """
def md5Sign(prestr, key) :
    prestr = "%s%s" % (prestr, key)
    m1 = md5.new()
    m1.update(prestr) 
    return m1.hexdigest()


"""
 * 验证签名
 * @param $prestr 需要签名的字符串
 * @param $sign 签名结果
 * @param $key 私钥
 * return 签名结果
 """
def md5Verify( prestr, sign, key) :
    prestr = "%s%s" % (prestr, key)
    m1 = md5.new()
    m1.update(prestr) 
    mysgin = m1.hexdigest()
    if mysgin == sign :
        return True
    else :
        return False