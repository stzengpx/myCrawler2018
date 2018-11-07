#!/user/bin/env python
# -*-coding:utf-8-*-
# @time       : 16/11/8 12:09
# @Author     : Zhangxy
# @File       : 001baiduSearch.py
# @Software   : PyCharm

#mac os＋selenium2＋chrome驱动＋python3 - zxy987872674的博客 - CSDN博客 - https://goo.gl/HwD7TJ
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
import csv
import codecs
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

# App Parameter
isDebugMode = True
isTurnOffChrome = True
timeoutImplicitlyWait = 20

# Search Criteria
myQryCond = "桃園"
myStartPage = 1
MyStopPage = 0 # 0 means all

#driver = webdriver.Chrome()
#driver.get("http://www.baidu.com")
#driver.find_element_by_id('kw').send_keys('selenium')
#driver.find_element_by_id('su').click()
#driver.quit()


# [Python] 使用Selenium在Google Chrome瀏覽器 @ Jialin :: 痞客邦 :: - https://goo.gl/TTv8C8
#web = webdriver.Chrome()
#web.get('http://www.cwb.gov.tw/V7/')
#web.set_window_position(0,0) #瀏覽器位置
#web.set_window_size(700,700) #瀏覽器大小
#time.sleep(5)
#web.find_element_by_link_text('天氣預報').click() #點擊頁面上"天氣預報"的連結
#time.sleep(5)
#web.close()

### Functions
def MyMoreLinkCollection(_workbook, _worksheet, _myweb, _PageCurrent):
    CountMoreLinkMouseOut = len(_myweb.find_elements_by_xpath("//*[@class='moreLinkMouseOut']"))
    # ListMoreLink = list()
    for i in range(1,CountMoreLinkMouseOut+1,1):
        try:
            DateTimeNow = datetime.datetime.now()
            # TmpMoreLink = myweb.find_element_by_xpath("(//*[@class='moreLinkMouseOut'])["+str(i)+"]").get_attribute("onclick")
            # ListMoreLink.append(TmpMoreLink)
            if isDebugMode : print("[頁,筆]: " + _PageCurrent + "," + str(i) + "," + str(DateTimeNow))
            # Scroll to Element
            # python - Scrolling to element using webdriver? - Stack Overflow - https://goo.gl/1Ci6uf
            element = _myweb.find_element_by_xpath("(//*[@class='moreLinkMouseOut'])["+str(i)+"]")
            _myweb.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            myweb.implicitly_wait(timeoutImplicitlyWait)
            TmpCorp  = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[4]").get_attribute("innerHTML")
            TmpAdd   = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[14]").get_attribute("innerHTML")
            TmpName  = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[16]").get_attribute("innerHTML")
            TmpCorp = TmpCorp[0:TmpCorp.index("<span")].strip()
            TmpAdd  = TmpAdd[0:TmpAdd.index("<span")].strip()
            TmpName = TmpName.strip()
            _worksheet.append([_PageCurrent,str(i),TmpCorp,TmpAdd,TmpName,str(DateTimeNow)])
            #保存
            _workbook.save(filename="data/myCrawler2018_" + str(DateTimeNowFile.strftime("%Y%m%d%H%M%S")) + ".xlsx")
            _myweb.back()
            myweb.implicitly_wait(timeoutImplicitlyWait)
            #time.sleep(1)
        except Exception as e:
            print('Error! MyMoreLinkCollection:' + str(i))
            print(e)
            continue

### Main

DateTimeNow     = datetime.datetime.now()
DateTimeNowFile = DateTimeNow
DateTimeStart   = DateTimeNow
DateTimeStop    = DateTimeNow
if isDebugMode : print(DateTimeNow)

### Python操作Excel新版本xlsx文件 | 不懂真人 - https://goo.gl/K8M7Eg
# 在内存中创建一个workbook对象，而且会至少创建一个 worksheet
wb = Workbook()
#获取当前活跃的worksheet,默认就是第一个worksheet
ws = wb.active
#可以使用append插入一行数据
#ws.append(['頁次','筆次','公司','地址','負責人','抓取時間'])

# Open the URL
myweb = webdriver.Chrome()
myweb.get('https://findbiz.nat.gov.tw/fts/query/QueryBar/queryInit.do')
myweb.implicitly_wait(timeoutImplicitlyWait)

# Search Criteria Entrance
myweb.find_element_by_id('qryCond').send_keys(myQryCond)
myweb.find_element_by_id('infoAddr').click()
myweb.find_element_by_xpath("//input[@value='factType']").click()
myweb.find_element_by_xpath("//input[@value='cmpyType']").click()
myweb.find_element_by_id('isAliveY').click()
ws.append(['qryCond','搜尋資料','資料種類4','登記現況'])
ws.append([myQryCond,'infoAddr','factType','isAliveY'])
ws.append(['頁次','筆次','公司','地址','負責人','抓取時間'])
myweb.find_element_by_id('qryBtn').click()

# Get Search Result Stats
DataRowsTotal = myweb.find_element_by_id('totalCount').get_attribute("value")
PageTotal     = myweb.find_element_by_id('totalPage').get_attribute("value")
PageCurrent   = myweb.find_element_by_id('currentPage').get_attribute("value")
if isDebugMode : print("DataRowsTotal: " + DataRowsTotal)
if isDebugMode : print("PageTotal: " + PageTotal)

PageTitle = ""
for i in range(myStartPage,int(PageTotal)+1,1):
    mygotoPage = "gotoPage(" + str(i)+ ");" 
    element = myweb.find_element_by_xpath("//a[@onclick='" + mygotoPage + "']")
    myweb.execute_script("arguments[0].scrollIntoView();", element)
    element.click()
    myweb.implicitly_wait(timeoutImplicitlyWait)
    time.sleep(1)
    # Check Title
    elementTitle = myweb.find_element_by_tag_name("title")
    elementTitleHtml = elementTitle.get_attribute("innerHTML")
    PageTitle = elementTitleHtml
    if isDebugMode : print("PageTitle: " + PageTitle)
    if PageTitle == "錯誤":
        myweb.back()
        i = i - 1
        time.sleep(5)
        continue
    # Go into detail
    PageCurrent   = myweb.find_element_by_id('currentPage').get_attribute("value")
    if isDebugMode : print("PageCurrent: " + PageCurrent)
    MyMoreLinkCollection(wb, ws, myweb, PageCurrent)
    if MyStopPage != 0 and i == MyStopPage : break
    

# print (myweb.find_element_by_class_name('moreLinkMouseOut').get_attribute("onclick"))
# myweb.find_element_by_xpath("(//*[@class='moreLinkMouseOut'])[""]")

# MyTable = [
#     ['公司', '地址', '負責人']
# ]

# myweb.find_element_by_class_name('moreLinkMouseOut').click()


### CSV
# Python 讀取與寫入 CSV 檔案教學與範例 - G. T. Wang - https://goo.gl/Pm7YbL
# How to declare and add items to an array in Python? - Stack Overflow - https://goo.gl/LzX8qt
# utf 8 - Write to UTF-8 file in Python - Stack Overflow - https://goo.gl/j8mXVT
# Python: 在CSV文件中写入中文字符 - 简书 - https://goo.gl/g1g9FM

### Google Sheet
# Python Quickstart  |  Sheets API  |  Google Developers - https://goo.gl/DTRI17
# Google Sheets API Client Library for Python  |  API Client Library for Python  |  Google Developers - https://goo.gl/TjWtDo
# 使用Python上傳資料到Google試算表 - 高中資訊科技概論教師黃建庭的教學網站 - https://goo.gl/EVu8xS
# Google Sheet With Python – 碼農勤耕田 – Medium - https://goo.gl/pVku9T
# 使用Python的上傳資料到谷歌試算表 – 一個人資料庫 - https://goo.gl/8jcsst
# 價格追蹤：使用 gspread 自動更新 Google Sheets · 翼之都 - https://goo.gl/tQbZfU


# Exit the app
DateTimeStop  = datetime.datetime.now()
if isDebugMode : print("Start: " + str(DateTimeStart))
if isDebugMode : print("Stop: "  + str(DateTimeStop))
if isDebugMode : print("Elapsed: " + str (DateTimeStop - DateTimeStart))
# time.sleep(0)
if isTurnOffChrome : myweb.quit()

'''
Reference:
4. 查找元素 — Selenium-Python中文文档 2 documentation - https://goo.gl/6yKn8g
Python String List Examples - Dot Net Perls - https://goo.gl/gb3Gjx
selenium-python-常用方法集锦（持续不断补充） - 程序园 - https://goo.gl/iCpob7
Python selenium —— 一定要会用selenium的等待，三种等待方式解读 « 灰蓝 - https://goo.gl/gUz7QL
网页处理实践（3）——python+selenium+firefox，不弹出窗口，静默模式运行 - qq_28053189的博客 - CSDN博客 - https://goo.gl/t1rGqu
'''