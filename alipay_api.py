#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015    liukelin
# @author: iiukelin      314566990@qq.com
import time
import alipay_config as alipay_config_class
from lib import alipay_submit_class
from lib import alipay_notify_class

#
# 请求支付
# @param request_data 请求post数据
# @return 支付跳转from表单
# WIDout_trade_no
# WIDsubject
# WIDtotal_fee
# WIDshow_url
# WIDbody
# WIDit_b_pay
# WIDextern_token
#
def alipay_pay(data = {}):
    config_ = alipay_config_class.alipay_config()

    time_ = time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))

    #支付类型
    payment_type = "1";
    #必填，不能修改
    #服务器异步通知页面路径
    notify_url = "http://xxxx.com/wap_alipay/alipay/notify_url.php"
    #需http://格式的完整路径，不能加?id=123这类自定义参数

    #页面跳转同步通知页面路径
    return_url = "http://xxxx.com/wap_alipay/alipay/return_url.php"
    #需http://格式的完整路径，不能加?id=123这类自定义参数，不能写成http://localhost/

    #商户订单号
    out_trade_no = data['WIDout_trade_no'] if data['WIDout_trade_no'] else time_       #$_POST['WIDout_trade_no'];
    #商户网站订单系统中唯一订单号，必填

    #订单名称
    subject = data['WIDsubject'] if data['WIDsubject'] else "test_%s" % out_trade_no   #$_POST['WIDsubject'];
    #必填

    #付款金额
    total_fee = data['WIDtotal_fee']      #$_POST['WIDtotal_fee'];
    #必填

    #商品展示地址
    show_url = data['WIDshow_url'] if data['WIDshow_url'] else 'http://qiandeer.com'     #$_POST['WIDshow_url'];
    #必填，需以http://开头的完整路径，例如：http://www.商户网址.com/myorder.html

    #订单描述
    body = data['WIDbody'] if data['WIDbody'] else "test order %s" % out_trade_no       #$_POST['WIDbody'];
    #选填

    #超时时间
    it_b_pay = data['WIDit_b_pay'] if data['WIDit_b_pay'] else 86400;       #$_POST['WIDit_b_pay'];
    #选填

    #钱包token
    extern_token = data['WIDextern_token'];
    #选填

    #构造要请求的参数数组，无需改动
    parameter = {
            "service"  : "alipay.wap.create.direct.pay.by.user",
            "partner": config_['partner'],
            "seller_id": config_['seller_id'],
            "payment_type": payment_type,
            "notify_url": notify_url,
            "return_url": return_url,
            "out_trade_no": out_trade_no,
            "subject": subject,
            "total_fee": total_fee,
            "show_url": show_url,
            "body": body,
            "it_b_pay": it_b_pay,
            "extern_token": extern_token,
            "_input_charset": config_['input_charset'].lower()
        }

    #建立请求
    alipaySubmit = alipay_submit_class.AlipaySubmit(config_)
    html_text = alipaySubmit.buildRequestForm(parameter, "get", "确认")
    return html_text

#
# 支付宝服务器异步通知
# @param request_data 请求post数据
# @return 
# *************************功能说明*************************
# 创建该页面文件时，请留心该页面文件中无任何HTML代码及空格。
# 该页面不能在本机电脑测试，请到服务器上做测试。请确保外部可以访问该页面。
# 该页面调试工具请使用写文本函数logResult，该函数已被默认关闭，见alipay_notify_class.php中的函数verifyNotify
# 如果没有收到该页面返回的 success 信息，支付宝会在24小时内按一定的时间策略重发通知
#post
def nottify_url(request_data) :
    config_ = alipay_config_class.alipay_config()
    #计算得出通知验证结果
    alipayNotify = alipay_notify_class.AlipayNotify(config_)
    verify_result = alipayNotify.verifyNotify(request_data)

    if verify_result : #验证成功
        #获取支付宝的通知返回参数，可参考技术文档中服务器异步通知参数列表
        
        #商户订单号
        out_trade_no = request_data['out_trade_no']

        #支付宝交易号
        trade_no = request_data['trade_no']

        #交易状态
        trade_status = request_data['trade_status']

        #"success"
        return True
    else :
        # "fail"
        return False



#
#支付宝页面跳转同步通知页面
# @param request_data 请求get数据
# @return 
# *************************页面功能说明*************************
# 该页面可在本机电脑测试
# 可放入HTML等美化页面的代码、商户业务逻辑程序代码
# 该页面可以使用PHP开发工具调试，也可以使用写文本函数logResult，该函数已被默认关闭，见alipay_notify_class.php中的函数verifyReturn
# get
def return_url(request_data) :

    config_ = alipay_config_class.alipay_config()
    #计算得出通知验证结果
    alipayNotify = alipay_notify_class.AlipayNotify(config_)
    verify_result = alipayNotify.verifyReturn(request_data)

    if verify_result :   #验证成功
        #商户订单号
        out_trade_no = request_data['out_trade_no'];

        #支付宝交易号
        trade_no = request_data['trade_no'];

        #交易状态
        trade_status = request_data['trade_status'];

        if request_data['trade_status'] == 'TRADE_FINISHED' or request_data['trade_status'] == 'TRADE_SUCCESS' :
            #判断该笔订单是否在商户网站中已经做过处理
            #如果没有做过处理，根据订单号（out_trade_no）在商户网站的订单系统中查到该笔订单的详细，并执行商户的业务程序
            #如果有做过处理，不执行商户的业务程序
            pass    
        return True
    else :
        #验证失败
        return False