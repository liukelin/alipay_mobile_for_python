#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015    liukelin
#
# @author: iiukelin      314566990@qq.com
# 
#  * 类名：AlipayNotify
#  * 功能：支付宝通知处理类
#  * 详细：处理支付宝各接口通知返回
#  * 说明：
#  * 以下代码只是为了方便商户测试而提供的样例代码，商户可以根据自己网站的需要，按照技术文档编写,并非一定要使用该代码。
#  * 该代码仅供学习和研究支付宝接口使用，只是提供一个参考

#  *************************注意*************************
#  * 调试通知返回时，可查看或改写log日志的写入TXT里的数据，来检查通知返回是否正常
import alipay_core_function
import alipay_md5_function

class AlipayNotify :
    
    # HTTPS形式消息验证地址
    https_verify_url = 'https://mapi.alipay.com/gateway.do?service=notify_verify&'
    
    #HTTP形式消息验证地址
    http_verify_url = 'http://notify.alipay.com/trade/notify_query.do?'
    alipay_config = ''

    def __init__(self, alipay_config) :
        self.alipay_config = alipay_config
    
    def AlipayNotify(self, alipay_config) :
        self.__init__(alipay_config)

     #
     # 针对notify_url验证消息是否是支付宝发出的合法消息
     # request_data 回传数据 (post)
     # @return 验证结果
     #
    def verifyNotify (self, request_data) :
        if len(request_data) ==0 :     #判断POST来的数组是否为空
            return False
        else :
            #生成签名结果
            isSign = self.getSignVeryfy(request_data, request_data["sign"])

            #获取支付宝远程服务器ATN结果（验证是否是支付宝发来的消息）
            responseTxt = 'false'
            if request_data["notify_id"]!='' :
                responseTxt = self.getResponse(self, request_data["notify_id"])
            
            #写日志记录
            #if ($isSign) {
            #  $isSignStr = 'true';
            # }else {
            #   $isSignStr = 'false';
            # }
            # $log_text = "responseTxt=".$responseTxt."\n notify_url_log:isSign=".$isSignStr.",";
            # $log_text = $log_text.createLinkString($_POST);
            # logResult($log_text);
            
            #验证
            #$responsetTxt的结果不是true，与服务器设置问题、合作身份者ID、notify_id一分钟失效有关
            #isSign的结果不是true，与安全校验码、请求时的参数格式（如：带自定义参数等）、编码格式有关
            #preg_match("/true$/i",$responseTxt) 
            if responseTxt == 'true' and isSign !='' :
                return True
            else :
                return False
    
    #
    # 针对return_url验证消息是否是支付宝发出的合法消息
    # @return 验证结果 (get)
    #
    def verifyReturn(self, request_data) :
        if len(request_data)==0 :      #判断POST来的数组是否为空
            return False
        else :
            #生成签名结果
            isSign = self.getSignVeryfy(request_data, request_data["sign"]);
            
            #获取支付宝远程服务器ATN结果（验证是否是支付宝发来的消息）
            responseTxt = 'false'
            if request_data["notify_id"] != '' :
                responseTxt = self.getResponse(self, request_data["notify_id"])
            #写日志记录
            # if ($isSign) {
            #   $isSignStr = 'true';
            # }
            # else {
            #   $isSignStr = 'false';
            # }
            # $log_text = "responseTxt=".$responseTxt."\n return_url_log:isSign=".$isSignStr.",";
            # $log_text = $log_text.createLinkString($_GET);
            # logResult($log_text);
            
            #验证
            #$responsetTxt的结果不是true，与服务器设置问题、合作身份者ID、notify_id一分钟失效有关
            #isSign的结果不是true，与安全校验码、请求时的参数格式（如：带自定义参数等）、编码格式有关
            #preg_match("/true$/i",$responseTxt) 
            if responseTxt == 'true' and isSign !='' :
                return True
            else :
                return False
    
    # 
    # 获取返回时的签名验证结果
    # @param para_temp 通知返回来的参数数组
    # @param sign 返回的签名结果
    # @return 签名验证结果
    # 
    def getSignVeryfy(self, para_temp,  sign) :
        #除去待签名参数数组中的空值和签名参数
        para_filter = alipay_core_function.paraFilter(para_temp)
        
        #对待签名参数数组排序
        keys = alipay_core_function.argSort(para_filter)
        
        #把数组所有元素，按照“参数=参数值”的模式用“&”字符拼接成字符串
        prestr = alipay_core_function.createLinkstring(para_filter, keys)
        
        isSgin = False
        if self.alipay_config['sign_type'].upper() == 'MD5':
            isSgin = alipay_md5_function.md5Verify(prestr, sign, self.alipay_config['key'])

        elif self.alipay_config['sign_type'].upper() == 'RSA':
            pass
        else :
            isSgin = False
        return isSgin

    #
    # 获取远程服务器ATN结果,验证返回URL
    # @param $notify_id 通知校验ID
    # @return 服务器ATN结果
    # 验证结果集：
    # invalid命令参数不对 出现这个错误，请检测返回处理中partner和key是否为空 
    # true 返回正确信息
    # false 请检查防火墙或者是服务器阻止端口问题以及验证时间是否超过一分钟
    # 
    def getResponse(self, notify_id) :
        transport = self.alipay_config['transport'].strip().lower()
        partner = self.alipay_config['partner'].strip()
        veryfy_url = ''
        
        if transport == 'https' :
            veryfy_url = self.https_verify_url
        else :
            veryfy_url = self.http_verify_url
        
        veryfy_url = "%spartner=%s&notify_id=%s" %(veryfy_url, partner, notify_id)
        responseTxt = alipay_core_function.getHttpResponseGET(veryfy_url, self.alipay_config['cacert'])
        
        return responseTxt

