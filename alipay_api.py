#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015    liukelin
import time
import alipay_config as alipay_config_class
from lib import alipay_submit_class
from lib import alipay_notify_class
from lib import alipay_md5_function

'''
  请求网页支付
  data = {
                    'WIDout_trade_no' : str(order_id),  #商户订单号
                    'WIDsubject' : desc,  #订单名称
                    'WIDtotal_fee'  : new_money,  #付款金额
                    'WIDshow_url'  : 'http://www.xxx.com',  #商品展示地址
                    'WIDbody'  : "msg:"+desc,  #订单描述
                    'WIDit_b_pay' : 10000,        #超时时间
                    'WIDextern_token' : '',   #钱包token
                    'notify_url':
                    'return_url':
            }
'''
def alipay_pay(data = {}):
    config_ = alipay_config_class.alipay_config()

    time_ = time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
    out_trade_no = data['WIDout_trade_no'] if data['WIDout_trade_no'] else ''
    if out_trade_no == '':
        return ''

    #支付类型
    payment_type = "1";
    #必填，不能修改
    #服务器异步通知页面路径
    notify_url =  data['notify_url']#"http://test.xxx.ymapp.com/pay/alipay_notify_url?ttoken=%s" % my_token
    #需http://格式的完整路径，不能加?id=123这类自定义参数

    #页面跳转同步通知页面路径
    return_url = data['return_url']
    #需http://格式的完整路径，不能加?id=123这类自定义参数，不能写成http://localhost/

    #商户订单号
    out_trade_no = data['WIDout_trade_no']       #$_POST['WIDout_trade_no'];
    #商户网站订单系统中唯一订单号，必填

    #订单名称
    subject = data['WIDsubject'] if data.has_key('WIDsubject') else "duobao_pay"   #$_POST['WIDsubject'];
    #必填

    #付款金额
    total_fee = data['WIDtotal_fee']      #$_POST['WIDtotal_fee'];
    #必填

    #商品展示地址
    show_url = data['WIDshow_url'] if data.has_key('WIDshow_url') else data['return_url']    #$_POST['WIDshow_url'];
    #必填，需以http://开头的完整路径，例如：http://www.商户网址.com/myorder.html

    #订单描述
    body = data['WIDbody'] if data.has_key('WIDbody') else "duobao_pay"       #$_POST['WIDbody'];
    #选填

    #超时时间
    it_b_pay = data['WIDit_b_pay'] if data.has_key('WIDit_b_pay') else 86400      #$_POST['WIDit_b_pay'];
    #选填

    #钱包token
    extern_token = data['WIDextern_token'] if data.has_key('WIDextern_token') else '';
    #选填

    #构造要请求的参数数组，无需改动
    parameter = {
            "service"  : "alipay.wap.create.direct.pay.by.user",
            # "service":'trade_create_by_buyer',
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
            # "it_b_pay": it_b_pay,
            # "extern_token": extern_token,
            # "antiphishing":'0',
            # "_input_charset": config_['input_charset'].lower()
        }

    #建立请求
    alipaySubmit = alipay_submit_class.AlipaySubmit(config_)

    # 返回 html from表单
    # html_text = alipaySubmit.buildRequestForm(parameter, "get", "确认")
    
    # 返回 支付 url
    html_text = alipaySubmit.buildRequestUrl(parameter)   
    return html_text

# 支付宝服务器异步通知
def nottify_url(request_data) :
    #计算得出通知验证结果
    config_ = alipay_config_class.alipay_config()
    #计算得出通知验证结果
    alipayNotify = alipay_notify_class.AlipayNotify(config_)
    verify_result = alipayNotify.verifyNotify(request_data)

    if verify_result :    #验证成功
        #批量付款数据中转账成功的详细信息
        # $success_details = $_POST['success_details'];
        # #批量付款数据中转账失败的详细信息
        # $fail_details = $_POST['fail_details'];
        # echo "success";  
        #调试用，写文本函数记录程序运行情况是否正常
        #logResult("这里写入想要调试的代码变量值，或其他运行的结果记录");
        return True
    else :
        #验证失败
        # "fail"
        return False

# 
def get_token(prestr):
    config_ = alipay_config_class.alipay_config()
    return alipay_md5_function.md5my_token(prestr, config_['key'])


def get_conf():
    config_ = alipay_config_class.alipay_config()
    alipay = {
            'seller_id' : config_['seller_id'],
            'key' :config_['key']  ,
            'partner':config_['partner'] ,
            'account_name': config_['account_name']
        }
    return alipay