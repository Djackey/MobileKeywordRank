# coding=utf-8

import requests
from bs4 import BeautifulSoup
import re
import random
import urllib
from random import choice
import pycurl
import StringIO
import urllib2
import string

AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12",
    "Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; zh-CN) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.302.2 Safari/532.8",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; zh-CN) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; zh-CN) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.15 Safari/534.13",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.2 (KHTML, like Gecko) Safari/125.8",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; fr-fr) AppleWebKit/312.5 (KHTML, like Gecko) Safari/312.3",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/418.8 (KHTML, like Gecko) Safari/419.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Camino/2.2.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0b6pre) Gecko/20100907 Firefox/4.0b6pre Camino/2.2a1pre",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.4 (KHTML like Gecko) Chrome/22.0.1229.79 Safari/537.4",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20120813 Firefox/16.0",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X; zh-CN) AppleWebKit/528.16 (KHTML, like Gecko, Safari/528.16) OmniWeb/v622.8.0.112941",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; zh-CN) AppleWebKit/528.16 (KHTML, like Gecko, Safari/528.16) OmniWeb/v622.8.0",
]


class BaiduRank:
    """docstring for BaiduRank"""

    def __init__(self):
        self.host = "www.baidu.com"
        self.UserAgent = choice(AGENTS)


    def curl(self, url, headers):
        while 1:
            try:
                c = pycurl.Curl()
                c.setopt(pycurl.MAXREDIRS, 5)
                c.setopt(pycurl.REFERER, url)
                c.setopt(pycurl.FOLLOWLOCATION, True)
                c.setopt(pycurl.CONNECTTIMEOUT, 120)
                c.setopt(pycurl.TIMEOUT, 120)
                c.setopt(pycurl.ENCODING, 'gzip,deflate')
                # c.setopt(c.PROXY,ip)       '''若使用代理，则取消本行注释'''
                c.fp = StringIO.StringIO()
                c.setopt(pycurl.URL, url)
                c.setopt(pycurl.HTTPHEADER, headers)
                c.setopt(pycurl.USERAGENT, self.UserAgent)
                c.setopt(c.WRITEFUNCTION, c.fp.write)
                c.perform()
                # code = c.getinfo(c.HTTP_CODE) 返回状态码
                html = c.fp.getvalue()
                if 'http://verify.baidu.com' in html:
                    print '出验证码,暂停10分钟'
                    time.sleep(1200)
                    continue
                else:
                    return html
            except Exception, what:
                information = '错误信息：%s' % what
                return str(information)
                continue

    def createURL(self, checkWord,page):  # create baidu URL with search words
        checkWord = checkWord.strip()
        # checkWord = checkWord.replace(' ', '+').replace('\n', '')
        # baiduURL = 'http://www.baidu.com/s?wd=%s&rn=50' % checkWord
        baidumobileurl = 'https://m.baidu.com/s?word=%s&pn=%s' % (checkWord,page)
        return baidumobileurl

    def getContent(self, baiduURL):  # get the content of the serp
        payload = [
            "Host: m.baidu.com",
            "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding: gzip, deflate, br",
            "Cookie: BAIDUID=AFB23F06A3C230D1B83BFD5F32EC53D8:FG=1; BIDUPSID=A1C6CA34DE59E7616BCB0E8520234ADA; PSTM=1475216597; BDUSS=VIVjB4bFdzNFJzVUFBc1JCLXlHdmR4MjdyVzRGeGN3aUwwUVYwbTA4TEl6eDlZQVFBQUFBJCQAAAAAAAAAAAEAAABsySg3tdrSu8e5QjJCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMhC-FfIQvhXWm; plus_cv=1::m:caa96deb; H_WISE_SIDS=110317_104496_100122_100103_108372_100097_109550_104340_109924_109700_107800_108453_109738_109557_110010_109682_110251_108013_107311_109657_110031_107242; BDRCVFR[gltLrB7qNCt]=mk3SLVN4HKm; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; plus_lsv=66d1a235e79e6dc1; BDICON=10123156; lsv=globalTjs_6281a6f-wwwTcss_ae234c8-routejs_6ede3cf-activityControllerjs_b6f8c66-wwwBcss_9f22dd4-framejs_6a98b69-globalBjs_9a6fc1f-sugjs_e1176fe-wwwjs_5d96b7e; MSA_WH=1440_763; MSA_PBT=92; MSA_ZOOM=1000; wpr=9"
            # "Cookie:BAIDUID=EC6ED338982C9DE1ED39972F1B4E5530:FG=1; BIDUPSID=EC6ED338982C9DE1ED39972F1B4E5530; PSTM=1434515748; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a01845311744; BDUSS=35KeW10a3pvNXdNMjQyVnhLUHFoYzZUSW9EVUF-ZXE1bUNuTXFFa0hTVU1tYWhWQVFBQUFBJCQAAAAAAAAAAAEAAADLTBsKYTYzMTM4MTcwMgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwMgVUMDIFVZ; ispeed_lsm=2; BD_HOME=1; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; BAIDUVERIFY=4606BC10EB2C2AB6D4B79FFA477238E38C5C6D295106222D2F75D4F8E9C766D5115D55C4E44133ACFE00D4768C6C1507E06B4C7D6221795299EE03FDE7CB2D46430000:1434541766:3f9b93890a7a5ed0; BDRCVFR[ltbVPlNi2ac]=mbxnW11j9Dfmh7GuZR8mvqV; BD_UPN=123253; sug=3; sugstore=1; ORIGIN=0; bdime=20100; H_PS_645EC=4093eiyri7wdn3v3qfviJa%2FFLXYwKxu%2FIF0wtL7d7pZ9maSmOTmtgqORRMlMRo7E; BD_CK_SAM=1; BDSVRTM=59; H_PS_PSSID=14795_1433_14602_14509_14444_14734_10812_12868_14622_14871_12723_14485_14919_14903_11664_13937_13189_10632",
            "Connection: keep-alive",
            "Upgrade-Insecure-Requests: 1"
        ]

        baidusshtml = self.curl(baiduURL, payload)
        return baidusshtml

    def getRank(self, checkWord, domain):  # main line
        strcheckWord = checkWord.replace('\n', '')
        pages = 0
        while pages < 51:
            checkWord = urllib.quote(strcheckWord)
            baiduURL = self.createURL(checkWord,pages)
            # print baiduURL
            cont = self.getContent(baiduURL)
            # print cont
            soup = BeautifulSoup(cont, "lxml")
            # print soup
            # zixungjc.write("%s\n" % soup)
            # find all results in this page
            results = soup.select(".results .result")
            # print results
            for result in results:
                # print result
                    # zixungjc.write("%s\n" % result)
                checkDatalist = result.select(".c-line-clamp1 .c-showurl")
                for checkData in checkDatalist:
                    pmwz = re.sub("<[^>]+>", "", str(checkData))
                    # print pmwz
                    # print checkData.string
                    if re.compile(r'(http://)?%s.*?' % domain).match("http://%s/?" % pmwz):
                        nowRank = result['order']
                        res = '%s(%s)' % (
                            strcheckWord,  string.atoi(nowRank)+pages)
                        return res
                        break
            else:
                pages = pages + 10

        return '%s(>50)' % strcheckWord


# baidurank = BaiduRank()
# domain = 'http://m.d17.cc'  # set the domain which you want to search.
# checkWord = '减压阀作用'
# rank = baidurank.getRank(checkWord, domain)
# print rank
