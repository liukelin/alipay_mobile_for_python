#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015    liukelin

import alipay_api

'''
    请求网页支付
'''
data = {
        'WIDout_trade_no' : '123123123',  #商户订单号
        'WIDtotal_fee'  : 1.0,  #付款金额
        'WIDshow_url'  : 'http://www.baidu.com',  #商品展示地址
        'notify_url': 'http://www.baidu.com' , # 异步回调地址
        'return_url': 'http://www.baidu.com',  #  同步跳转地址
}

# pay_url 生成网页支付 url
pay_url = alipay_api.alipay_pay(data)