#!/usr/local/bin/python
#-*-coding:utf-8-*-

import xdrlib
import sys
import xlrd
from pmchaxun import BaiduRank
from xlutils.copy import copy
import time
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

baidurank = BaiduRank()

# domain = 'www.jmtyzs.net/'  # set the domain which you want to search.
# checkWord = '南昌庭院装饰'
# rank = baidurank.getRank(checkWord, domain)
# print rank
# 打开excel 文件


class ExcelRank:
    """docstring for ClassName"""

    def excelbaidurank(self,xlsname, addrownum):
        data = xlrd.open_workbook(xlsname)
        # 通过名称获取工作表
        table = data.sheet_by_name(u'Sheet1')
        # 获取表格的行数和列数
        rankbigger50 = 0
        ranklarger50 = 0
        nrows = table.nrows
        # nrows = 2
        ncols = table.ncols
        cxurl_data = []
        cxgjc_data = []
        gjcpm_data = []

        for i in range(nrows):
            # 获取一行的数据，返回数组
            row_values = table.row_values(i)
            cxurl_data.append(row_values[0])
            cxgjc_data.append(row_values[2])
            gjclist = cxgjc_data[i]
            m = re.split(',', gjclist)
            gjcpm_data.append(m)
            for a in range(0, len(gjcpm_data[i])):
                rank = baidurank.getRank(
                    gjcpm_data[i][a].encode('utf-8'), cxurl_data[i])
                print rank
                if "(>50)" in rank:
                    rankbigger50 += 1
                else:
                    ranklarger50 += 1
                oldWb = xlrd.open_workbook(xlsname, formatting_info=True)
                newWb = copy(oldWb)
                newWs = newWb.get_sheet(0)
                newWs.write(i, addrownum + 3 + a, "%s" % unicode(rank))
                print "write new values ok"
                newWb.save(xlsname)
                print "save with same name ok"
        zixunpmdict = {'rankbigger50': rankbigger50,
                       'ranklarger50': ranklarger50}
        return zixunpmdict

    def GetNowTime(self):
        return time.strftime("%Y-%m-%d", time.localtime(time.time()))

excelrank = ExcelRank()
nowtime = str(excelrank.GetNowTime())

xlsnamelist = ['08240914news.xls', '09141013news.xls', '10141031news.xls']
# xlsnamelist = ['test.xls']

for xlsname in xlsnamelist:
    txtmm = xlsname.replace('.xls', '')
    zixunpmtxt = open('%spmqk.txt' % txtmm, 'a')
    addrownum = 1
    print xlsname
    pmnum = excelrank.excelbaidurank(xlsname, addrownum)
    rankl50 = pmnum['ranklarger50']
    rankb50 = pmnum['rankbigger50']
    pmlv = str(round(float(rankl50) / float(rankl50 + rankb50) * 100, 2))
    # print pmlv
    zixunpmtxt.write('%s 关键词排名大于(50)的数量%s 关键词排名小于(50)的数量%s 排名率为%s\n' %
                     (nowtime, rankb50, rankl50, pmlv))
