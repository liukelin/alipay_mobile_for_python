#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015    liukelin
# @author: iiukelin      314566990@qq.com
import time
import alipay_config as alipay_config_class
from lib import alipay_submit_class

def alipay_api(data = {}):
    config_ = alipay_config_class.alipay_config()

    time_ = time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))

    #支付类型
    payment_type = "1";
    #必填，不能修改
    #服务器异步通知页面路径
    notify_url = "http://test.qiandeer.ymapp.com/wap_alipay/alipay/notify_url.php"
    #需http://格式的完整路径，不能加?id=123这类自定义参数

    #页面跳转同步通知页面路径
    return_url = "http://test.qiandeer.ymapp.com/wap_alipay/alipay/return_url.php"
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