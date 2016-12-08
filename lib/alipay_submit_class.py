#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015    liukelin
#
# @author: iiukelin      314566990@qq.com
# """
#  * 类名：AlipaySubmit
#  * 功能：支付宝各接口请求提交类
#  * 详细：构造支付宝各接口表单HTML文本，获取远程HTTP数据
#  * 说明：
#  * 以下代码只是为了方便商户测试而提供的样例代码，商户可以根据自己网站的需要，按照技术文档编写,并非一定要使用该代码。
#  * 该代码仅供学习和研究支付宝接口使用，只是提供一个参考。
#  """
import alipay_core_function
import alipay_md5_function

class AlipaySubmit:
    alipay_config = ""
    #支付宝网关地址（新）
    alipay_gateway_new = 'https://mapi.alipay.com/gateway.do?'

    def __init__(self, alipay_config) :
        self.alipay_config = alipay_config

    def AlipaySubmit(self, alipay_config) :
        self.__init__(alipay_config)

     # """
     # * 生成签名结果
     # * @param $para_sort 已排序要签名的数组
     # * return 签名结果字符串
     # """
    def buildRequestMysign(self, para_sort) :

        #对待签名参数数组排序
        keys = alipay_core_function.argSort(para_sort)

        #把数组所有元素，按照“参数=参数值”的模式用“&”字符拼接成字符串
        prestr = alipay_core_function.createLinkstring(para_sort, keys)


        print "==%s=%s==" %(para_sort, prestr)
        if self.alipay_config['sign_type'].upper()  == 'MD5':
            mysign = alipay_md5_function.md5Sign(prestr, self.alipay_config['key'])
        else :
            mysign = ""
        return mysign

     # """
     # * 生成要请求给支付宝的参数数组
     # * @param $para_temp 请求前的参数数组
     # * @return 要请求的参数数组
     # """
    def buildRequestPara(self, para_temp) :
        #除去待签名参数数组中的空值和签名参数
        para_sort = alipay_core_function.paraFilter(para_temp)

        #生成签名结果
        mysign = self.buildRequestMysign(para_sort)
        
        # print "para_filter:%s,para_sort:%s,mysign:%s" %(para_filter,para_sort,mysign)

        #签名结果与签名方式加入请求提交参数组中
        para_sort['sign'] = mysign;
        para_sort['sign_type'] = self.alipay_config['sign_type'].upper()
        
        return para_sort

    # 
    #  建立请求，以表单HTML形式构造（默认）
    #  @param $para_temp 请求参数数组
    #  @param $method 提交方式。两个值可选：post、get
    #  @param $button_name 确认按钮显示文字
    #  @return 提交表单HTML文本
    # 
    def buildRequestForm(self, para_temp, method, button_name) :

        # print "===%s=%s=%s=%s====" %(self.alipay_config,para_temp, method, button_name )

        #待请求参数数组
        para = self.buildRequestPara(para_temp)
        sHtml = """<form id='alipaysubmit' name='alipaysubmit' action='%s_input_charset=%s' method='%s'  target="_blank">""" \
                        %( self.alipay_gateway_new, self.alipay_config['input_charset'].lower() , method)
        for k in para :
            sHtml += "<input type='hidden' name='%s' value='%s'/>" %(str(k), str(para[k]))

        #submit按钮控件请不要含有name属性
        sHtml = "%s<input type='submit' value='%s'></form>" %(sHtml , button_name)
        # sHtml = "%s<script>document.forms['alipaysubmit'].submit();</script>" %(sHtml)
        return sHtml


    # 建立请求，以URL形式构造
    def buildRequestUrl(self, para_temp):
        import urllib

        # url = "%s_input_charset=%s" %(self.alipay_gateway_new, self.alipay_config['input_charset'].lower())
        #待请求参数数组
        para = self.buildRequestPara(para_temp)
        # print para
        # for k in para :
        #     url += "&%s=%s" %(str(k), str(para[k]) )
        data = "&%s" % urllib.urlencode(para)
        # import requests
        # m = requests.post( url, para ) 
        # url = m.text.decode("utf-8")
        return self.alipay_gateway_new +'?'+ data


    # 
    #  * 建立请求，以模拟远程HTTP的POST请求方式构造并获取支付宝的处理结果
    #  * @param $para_temp 请求参数数组
    #  * @return 支付宝处理结果
    #  
    def buildRequestHttp(self, para_temp) :
        sResult = ''
        #待请求参数数组字符串
        request_data = self.buildRequestPara(para_temp)
        #远程获取数据
        sResult = alipay_core_function.getHttpResponsePOST(self.alipay_gateway_new, self.alipay_config['cacert'],  request_data, self.alipay_config['input_charset'].lower() )
        return sResult
    #
    # * 建立请求，以模拟远程HTTP的POST请求方式构造并获取支付宝的处理结果，带文件上传功能
    # * @param $para_temp 请求参数数组
    # * @param $file_para_name 文件类型的参数名
    # * @param $file_name 文件完整绝对路径
    # * @return 支付宝返回处理结果
    #
    def buildRequestHttpInFile(self, para_temp, file_para_name, file_name) :
        
        #待请求参数数组
        para = self.buildRequestPara(para_temp);
        para[file_para_name] = "@%s" % file_name
        
        #远程获取数据
        sResult = alipay_core_function.getHttpResponsePOST(self.alipay_gateway_new,  self.alipay_config['cacert'],  para, self.alipay_config['input_charset'].lower());

        return sResult

    # 
    #  用于防钓鱼，调用接口query_timestamp来获取时间戳的处理函数
    #  注意：该功能PHP5环境及以上支持，因此必须服务器、本地电脑中装有支持DOMDocument、SSL的PHP配置环境。建议本地调试时使用PHP开发软件
    #  return 时间戳字符串
    # 
    def query_timestamp(self) :
        url = "%sservice=query_timestamp&partner=%s&_input_charset=%s" %(self.alipay_gateway_new, self.alipay_config['partner'].lower(), self.alipay_config['input_charset'].lower() )
        encrypt_key = ""

        # $doc = new DOMDocument();
        # $doc->load($url);
        # $itemEncrypt_key = $doc->getElementsByTagName( "encrypt_key" );
        # $encrypt_key = $itemEncrypt_key->item(0)->nodeValue;
        return encrypt_key
