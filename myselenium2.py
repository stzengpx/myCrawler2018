#!/user/bin/env python
# -*-coding:utf-8-*-
# @time       : 2018/10/24
# @Author     : Patrick Tseng
# @File       : myselenium2.py
# @Software   : VSCode
# mac os＋selenium2＋chrome驱动＋python3 - zxy987872674的博客 - CSDN博客 - https://goo.gl/HwD7TJ

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
import csv
import codecs
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
import sys
import subprocess
import smtplib
from email.mime.text import MIMEText
import urllib.parse
import urllib.request
import json
from bs4 import BeautifulSoup

### Class
class myselenium2():
    def __init__(self):
        
        # App Parameter
        self.isDebugMode = True
        self.isTurnOffChrome = True
        self.timeoutImplicitlyWait = 30

        self.myQryCond       = ""
        self.myStartPage     = ""
        self.myStopPage      = ""
        self.myDataType      = ""
        self.myDataType1     = ""
        self.myDataType2     = ""
        self.myDataType3     = ""
        self.myDataType4     = ""
        self.myDataType5     = ""
        self.myTurnOffChrome = ""
        self.myHeadlessMode  = ""
        
        self.isTurnOffChrome = True if self.myTurnOffChrome == "0" else False
        
        ### tables for log
        self.tableMylog = [['','','','','']] # ['DateTime', 'qryCond', 'DataRowsTotal', 'PageTotal', 'PageCurrent']
        self.tableMyError = []

        # App History
        ## self.officialSiteVersion = "1.2.9" # 20181101
        ## self.officialSiteVersion = "1.3.1" # 20181113
        ## self.officialSiteVersion = "1.3.5" # 20200108
        self.officialSiteVersion = "1.3.6" # 20200430
    
        self.myAppVersion = "2020043001"
        
        self.serial_number = self.getSerialNumber()
    
    def getSerialNumber(self):
        # macos - Using Python to find Mac UUID/Serial Number - Stack Overflow - https://goo.gl/hY6XrS
        cmd = "system_profiler SPHardwareDataType | grep 'Serial Number' | awk '{print $4}'"
        result = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True, check=True)
        serial_number = result.stdout.strip()
        return serial_number

    def mySendMailUsage(self):
        try:
            # 使用 Python 寄發 Gmail | Yu-Cheng Huang - https://goo.gl/ELX55X
            # import smtplib
            # from email.mime.text import MIMEText
            
            gmail_user = 'smtpzengpx@gmail.com'
            #gmail_password = '1qaz@WSX3edc' # your gmail password
            gmail_password = 'ygvfikiwcdyykboj' # 20200108 應用程式密碼 https://support.google.com/accounts/answer/185833

            msgContent = 'Login - ' + self.serial_number.decode("utf-8")
            msgContent += '\r\n' + 'myQryCond: ' + self.myQryCond
            msgContent += '\r\n' + 'myStartPage: ' + str(self.myStartPage)
            msgContent += '\r\n' + 'myStopPage: ' + str(self.myStopPage)
            msgContent += '\r\n' + 'myDataType: ' + self.myDataType
            msgContent += '\r\n' + 'myTurnOffChrome: ' + self.myTurnOffChrome
            msgContent += '\r\n' + 'myHeadlessMode: ' + self.myHeadlessMode
            msg = MIMEText(msgContent)
            msg['Subject'] = 'myCrawler2018_user_' + self.serial_number.decode("utf-8") 
            msg['From'] = gmail_user
            msg['To'] = 'st.zengpx@gmail.com'
            
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.send_message(msg)
            server.quit()
            
            print(self.serial_number.decode("utf-8") + ' - Login alert was sent.')
        except Exception as e:
            print (e)
            print ('Warning! Login aler was not sent...')

    def myCheckTitle(self, _myweb):
        # Check Title
        # print("check title")
        elementTitle = _myweb.find_element_by_tag_name("title")
        elementTitleHtml = elementTitle.get_attribute("innerHTML")
        PageTitle = elementTitleHtml
        if PageTitle == "錯誤" :
            print("PageTitle == 錯誤")
            time.sleep(1)
            _myweb.back()
            _myweb.implicitly_wait(self.timeoutImplicitlyWait)
        return PageTitle

    def MyMoreLinkCollection(self, _workbook, _worksheet, _myweb, _PageCurrent):
        CountMoreLinkMouseOut = len(_myweb.find_elements_by_xpath("//*[@class='moreLinkMouseOut']"))
        # ListMoreLink = list()
        TmpStockStatus = ""
        TmpAmountReal = ""
        TmpPageTitleTest = ""
        i = 1
        while i < CountMoreLinkMouseOut+1 :
        #for i in range(1,CountMoreLinkMouseOut+1,1):
            # if TmpPageTitleTest == "錯誤" : i = i - 1
            try:
                DateTimeNow = datetime.datetime.now()
                # TmpMoreLink = myweb.find_element_by_xpath("(//*[@class='moreLinkMouseOut'])["+str(i)+"]").get_attribute("onclick")
                # ListMoreLink.append(TmpMoreLink)
                if self.isDebugMode : print("[頁,筆]: " + _PageCurrent + "," + str(i) + "," + str(DateTimeNow))
                # Scroll to Element
                # python - Scrolling to element using webdriver? - Stack Overflow - https://goo.gl/1Ci6uf
                element = _myweb.find_element_by_xpath("(//*[@class='moreLinkMouseOut'])["+str(i)+"]")
                _myweb.execute_script("arguments[0].scrollIntoView();", element)
                element.click()
                _myweb.implicitly_wait(self.timeoutImplicitlyWait)
                TmpPageTitleTest = self.myCheckTitle(_myweb)
                # if isDebugMode: print ("TmpPageTitleTest: " + TmpPageTitleTest)
                if TmpPageTitleTest == "錯誤" : 
                    _myweb.back()
                    _myweb.implicitly_wait(self.timeoutImplicitlyWait)
                    continue
                TmpDataType = _myweb.find_element_by_xpath("//*[@class='tab-content']/div/h3").get_attribute("innerHTML")
                TmpDataType = TmpDataType.strip()
                # print(TmpDataType)
                if TmpDataType == "工廠基本資料":
                    TmpCorp     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[4]").get_attribute("innerHTML")
                    TmpAdd      = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[14]").get_attribute("innerHTML")
                    TmpName     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[16]").get_attribute("innerHTML")
                    TmpCorp     = TmpCorp[0:TmpCorp.index("<span")].strip()
                    TmpAdd      = TmpAdd[0:TmpAdd.index("<span")].strip()
                    TmpName     = TmpName.strip()
                elif TmpDataType == "商業登記基本資料":
                    # print("2")
                    TmpPartnerHead = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[13]").get_attribute("innerHTML")
                    TmpPartnerHead = TmpPartnerHead.strip()
                    if TmpPartnerHead == "合夥人姓名":
                        TmpCorp     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[10]").get_attribute("innerHTML")
                        TmpAdd      = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[22]").get_attribute("innerHTML")
                        #TmpName     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[12]").get_attribute("innerHTML")
                        TmpName     = _myweb.find_element_by_xpath("//*[@id='tabBusmContent']/div/table/tbody/tr[6]/td[2]/table/tbody/tr/td[1]").get_attribute("innerHTML")
                        TmpCorp     = TmpCorp[0:TmpCorp.index("<span")].strip()
                        TmpAdd      = TmpAdd[0:TmpAdd.index('<span')].strip()
                        TmpName     = TmpName.strip()
                    else:
                        TmpCorp     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[10]").get_attribute("innerHTML")
                        TmpAdd      = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[20]").get_attribute("innerHTML")
                        #TmpName     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[12]").get_attribute("innerHTML")
                        TmpName     = _myweb.find_element_by_xpath("//*[@id='tabBusmContent']/div/table/tbody/tr[6]/td[2]/table/tbody/tr/td[1]").get_attribute("innerHTML")
                        TmpCorp     = TmpCorp[0:TmpCorp.index("<span")].strip()
                        TmpAdd      = TmpAdd[0:TmpAdd.index('<span')].strip()
                        TmpName     = TmpName.strip()
                elif TmpDataType == "分公司資料":
                    # print("3")
                    TmpCorp     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[18]").get_attribute("innerHTML")
                    TmpAdd      = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[10]").get_attribute("innerHTML")
                    TmpName     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[8]").get_attribute("innerHTML")
                    TmpCorp     = TmpCorp[TmpCorp.index('">')+2:TmpCorp.index("</a>")].strip()
                    TmpAdd      = TmpAdd[0:TmpAdd.index('<span')].strip()
                    TmpName     = TmpName.strip()
                elif TmpDataType == "外國公司登記基本資料":
                    TmpCorp     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[6]").get_attribute("innerHTML")
                    TmpAdd      = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[12]").get_attribute("innerHTML")
                    TmpName     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[10]").get_attribute("innerHTML")
                    TmpCorp     = TmpCorp[0:TmpCorp.index("<span")].strip()
                    TmpAdd      = TmpAdd[0:TmpAdd.index("<span")].strip()
                    TmpName     = TmpName.strip()
                elif TmpDataType == "外國公司報備基本資料":
                    # print("4")
                    TmpCorp     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[6]").get_attribute("innerHTML")
                    TmpAdd      = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[10]").get_attribute("innerHTML")
                    TmpName     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[8]").get_attribute("innerHTML")
                    TmpCorp     = TmpCorp[0:TmpCorp.index("<span")].strip()
                    TmpAdd      = TmpAdd[0:TmpAdd.index("<span")].strip()
                    TmpName     = TmpName.strip()
                elif TmpDataType == "外國公司認許基本資料":
                    TmpCorpHeader = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[5]").get_attribute("innerHTML")
                    TmpCorpHeader = TmpCorpHeader.strip()
                    if TmpCorpHeader == "公司名稱":
                        TmpCorp     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[6]").get_attribute("innerHTML")
                        TmpAdd      = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[12]").get_attribute("innerHTML")
                        TmpName     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[10]").get_attribute("innerHTML")
                        TmpCorp     = TmpCorp[0:TmpCorp.index("<span")].strip()
                        TmpAdd      = TmpAdd[0:TmpAdd.index("<span")].strip()
                        TmpName     = TmpName.strip()
                    else:
                        TmpCorp     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[8]").get_attribute("innerHTML")
                        TmpAdd      = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[14]").get_attribute("innerHTML")
                        TmpName     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[12]").get_attribute("innerHTML")
                        TmpCorp     = TmpCorp[0:TmpCorp.index("<span")].strip()
                        TmpAdd      = TmpAdd[0:TmpAdd.index("<span")].strip()
                        TmpName     = TmpName.strip()
                elif TmpDataType == "外國公司辦事處登記基本資料": # 20200504
                    TmpCorp     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[6]").get_attribute("innerHTML")
                    TmpAdd      = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[10]").get_attribute("innerHTML")
                    TmpName     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[8]").get_attribute("innerHTML")
                    TmpCorp     = TmpCorp[0:TmpCorp.index("<span")].strip()
                    TmpAdd      = TmpAdd[0:TmpAdd.index("<span")].strip()
                    TmpName     = TmpName.strip()
                elif TmpDataType == "公司基本資料":
                    # print("5")
                    TmpStockStatus = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[6]").get_attribute("innerHTML")
                    TmpStockStatus = TmpStockStatus.strip()
                    TmpCorpType    = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[9]").get_attribute("innerHTML")
                    TmpCorpType    = TmpCorpType.strip()
                    TmpAmountReal  = ""
                    if TmpCorpType == "公司屬性":
                        TmpAmountReal = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[13]").get_attribute("innerHTML")
                        TmpAmountReal = TmpAmountReal.strip()
                    else:
                        TmpAmountReal = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[11]").get_attribute("innerHTML")
                        TmpAmountReal = TmpAmountReal.strip()
                    if TmpStockStatus == "僑外資":
                        TmpAmountReal = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[15]").get_attribute("innerHTML")
                        TmpAmountReal = TmpAmountReal.strip()
                        if TmpAmountReal == "實收資本額(元)" :
                            TmpCorp     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[10]").get_attribute("innerHTML")
                            TmpAdd      = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[20]").get_attribute("innerHTML")
                            TmpName     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[18]").get_attribute("innerHTML")
                            TmpCorp     = TmpCorp[0:TmpCorp.index("<span")].strip()
                            TmpAdd      = TmpAdd[0:TmpAdd.index("<span")].strip()
                            TmpName     = TmpName.strip()
                        else:
                            TmpCorp     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[8]").get_attribute("innerHTML")
                            TmpAdd      = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[18]").get_attribute("innerHTML")
                            TmpName     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[16]").get_attribute("innerHTML")
                            TmpCorp     = TmpCorp[0:TmpCorp.index("<span")].strip()
                            TmpAdd      = TmpAdd[0:TmpAdd.index("<span")].strip()
                            TmpName     = TmpName.strip()
                            #print(TmpCorp)
                            #print(TmpName)
                            #quit()
                    elif TmpAmountReal == "實收資本額(元)" :
                        if TmpCorpType == "公司屬性":
                            TmpCorp     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[6]").get_attribute("innerHTML")
                            TmpAdd      = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[18]").get_attribute("innerHTML")
                            TmpName     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[16]").get_attribute("innerHTML")
                            TmpCorp     = TmpCorp[0:TmpCorp.index("<span")].strip()
                            TmpAdd      = TmpAdd[0:TmpAdd.index("<span")].strip()
                            TmpName     = TmpName.strip()                        
                        else:
                            TmpCorp     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[6]").get_attribute("innerHTML")
                            TmpAdd      = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[16]").get_attribute("innerHTML")
                            TmpName     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[14]").get_attribute("innerHTML")
                            TmpCorp     = TmpCorp[0:TmpCorp.index("<span")].strip()
                            TmpAdd      = TmpAdd[0:TmpAdd.index("<span")].strip()
                            TmpName     = TmpName.strip()
                    else:
                        TmpCorp     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[6]").get_attribute("innerHTML")
                        TmpAdd      = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[14]").get_attribute("innerHTML")
                        TmpName     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[12]").get_attribute("innerHTML")
                        TmpCorp     = TmpCorp[0:TmpCorp.index("<span")].strip()
                        TmpAdd      = TmpAdd[0:TmpAdd.index("<span")].strip()
                        TmpName     = TmpName.strip()
                elif TmpDataType == "有限合夥登記基本資料":
                    # print("6")
                    TmpCorp     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[6]").get_attribute("innerHTML")
                    TmpAdd      = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[8]").get_attribute("innerHTML")
                    #TmpName     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[20]").get_attribute("innerHTML")
                    TmpName     = _myweb.find_element_by_xpath("//*[@id='tabBusmContent']/div/table/tbody/tr[10]/td[2]/table/tbody/tr/td[1]").get_attribute("innerHTML")
                    TmpCorp     = TmpCorp[0:TmpCorp.index("<span")].strip()
                    TmpAdd      = TmpAdd[0:TmpAdd.index('<span')].strip()
                    TmpName     = TmpName.strip()
                    # print(TmpCorp)
                    # print(TmpAdd)
                    # print(TmpName)
                    # quit()
                elif TmpDataType == "商業登記基本資料(分支機構)":
                    TmpCorp     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[10]").get_attribute("innerHTML")
                    TmpAdd      = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[16]").get_attribute("innerHTML")
                    TmpName     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[12]").get_attribute("innerHTML")
                    #TmpName     = _myweb.find_element_by_xpath("//*[@id='tabBusmContent']/div/table/tbody/tr[6]/td[2]/table/tbody/tr/td[1]").get_attribute("innerHTML")
                    TmpCorp     = TmpCorp[0:TmpCorp.index("<span")].strip()
                    TmpAdd      = TmpAdd[0:TmpAdd.index('<span')].strip()
                    TmpName     = TmpName.strip()
                    # quit()
                elif TmpDataType == "大陸公司許可基本資料":
                    TmpCorp     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[8]").get_attribute("innerHTML")
                    TmpAdd      = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[16]").get_attribute("innerHTML")
                    TmpName     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[14]").get_attribute("innerHTML")
                    #TmpName     = _myweb.find_element_by_xpath("//*[@id='tabBusmContent']/div/table/tbody/tr[6]/td[2]/table/tbody/tr/td[1]").get_attribute("innerHTML")
                    TmpCorp     = TmpCorp[0:TmpCorp.index("<span")].strip()
                    TmpAdd      = TmpAdd[0:TmpAdd.index('<span')].strip()
                    TmpName     = TmpName.strip()
                    #quit()
                elif TmpDataType == "大陸公司許可報備基本資料":
                    TmpCorp     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[8]").get_attribute("innerHTML")
                    TmpAdd      = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[14]").get_attribute("innerHTML")
                    TmpName     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[12]").get_attribute("innerHTML")
                    #TmpName     = _myweb.find_element_by_xpath("//*[@id='tabBusmContent']/div/table/tbody/tr[6]/td[2]/table/tbody/tr/td[1]").get_attribute("innerHTML")
                    TmpCorp     = TmpCorp[0:TmpCorp.index("<span")].strip()
                    TmpAdd      = TmpAdd[0:TmpAdd.index('<span')].strip()
                    TmpName     = TmpName.strip()
                    #quit()
                else:
                    '''
                    大陸公司許可基本資料 台北市內湖區 459,8
                    商業登記基本資料(分支機構) 桃園 100,9
                    大陸公司許可報備基本資料 桃園 478,5
                    '''
                    print("TmpDataType: " + TmpDataType)
                    print("TmpDataType not found")
                    _worksheet.append([_PageCurrent,str(i),"TmpDataTypeNotFound","TmpDataTypeNotFound","TmpDataTypeNotFound",TmpDataType,str(DateTimeNow)])
                    i = i + 1
                    _myweb.back()
                    _myweb.implicitly_wait(self.timeoutImplicitlyWait)
                    self.myCheckTitle(_myweb)
                    # if isDebugMode: quit()
                    self.tableMyError.append([str(DateTimeNow),TmpDataType,_PageCurrent,str(i)])
                    continue
                # quit()
                _worksheet.append([_PageCurrent,str(i),TmpCorp,TmpAdd,TmpName,TmpDataType,str(DateTimeNow)])
                #time.sleep(1)
                _myweb.back()
                _myweb.implicitly_wait(self.timeoutImplicitlyWait)
                self.myCheckTitle(_myweb)
                i = i + 1
                #time.sleep(1)
            except Exception as e:
                try:
                    if TmpStockStatus == "僑外資":
                        TmpCorp     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[8]").get_attribute("innerHTML")
                        TmpAdd      = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[16]").get_attribute("innerHTML")
                        TmpName     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[14]").get_attribute("innerHTML")
                        TmpCorp     = TmpCorp[0:TmpCorp.index("<span")].strip()
                        TmpAdd      = TmpAdd[0:TmpAdd.index("<span")].strip()
                        TmpName     = TmpName.strip()
                    else:
                        print('Error! MyMoreLinkCollection1:' + str(i))
                        print(e)
                        self.tableMyError.append([str(DateTimeNow),self.myQryCond,self.myStartPage,self.myStopPage,self.myDataType,'Error! MyMoreLinkCollection1',TmpDataType,_PageCurrent,str(i)])
                    _myweb.back()
                    _myweb.implicitly_wait(self.timeoutImplicitlyWait)
                    self.myCheckTitle(_myweb)
                    i = i + 1
                    # quit()
                    continue
                except Exception as e:
                    print('Error! MyMoreLinkCollection2:' + str(i))
                    print(e)
                    self.tableMyError.append([str(DateTimeNow),self.myQryCond,self.myStartPage,self.myStopPage,self.myDataType,'Error! MyMoreLinkCollection2',TmpDataType,_PageCurrent,str(i)])
                    _myweb.back()
                    _myweb.implicitly_wait(self.timeoutImplicitlyWait)
                    self.myCheckTitle(_myweb)
                    i = i + 1
                    continue

    def MyMoreLinkCollection2(self, _workbook, _worksheet, _myweb, _PageCurrent):
        CountMoreLinkMouseOut = len(_myweb.find_elements_by_xpath("//*[@class='moreLinkMouseOut']"))
        # ListMoreLink = list()
        TmpStockStatus = ""
        TmpAmountReal = ""
        TmpPageTitleTest = ""
        i = 1
        while i < CountMoreLinkMouseOut+1 :
        #for i in range(1,CountMoreLinkMouseOut+1,1):
            # if TmpPageTitleTest == "錯誤" : i = i - 1
            try:
                DateTimeNow = datetime.datetime.now()
                # TmpMoreLink = myweb.find_element_by_xpath("(//*[@class='moreLinkMouseOut'])["+str(i)+"]").get_attribute("onclick")
                # ListMoreLink.append(TmpMoreLink)
                if self.isDebugMode : print("[頁,筆]: " + _PageCurrent + "," + str(i) + "," + str(DateTimeNow))
                # Scroll to Element
                # python - Scrolling to element using webdriver? - Stack Overflow - https://goo.gl/1Ci6uf
                element = _myweb.find_element_by_xpath("(//*[@class='moreLinkMouseOut'])["+str(i)+"]")
                _myweb.execute_script("arguments[0].scrollIntoView();", element)
                element.click()
                _myweb.implicitly_wait(self.timeoutImplicitlyWait)
                TmpPageTitleTest = self.myCheckTitle(_myweb)
                # if isDebugMode: print ("TmpPageTitleTest: " + TmpPageTitleTest)
                if TmpPageTitleTest == "錯誤" : 
                    _myweb.back()
                    _myweb.implicitly_wait(self.timeoutImplicitlyWait)
                    continue
                TmpCorp,TmpAdd,TmpName = ""
                TmpDataType = _myweb.find_element_by_xpath("//*[@class='tab-content']/div/h3").get_attribute("innerHTML")
                TmpDataType = TmpDataType.strip()
                _worksheet.append([_PageCurrent,str(i),TmpCorp,TmpAdd,TmpName,TmpDataType,str(DateTimeNow)])
                #time.sleep(1)
                _myweb.back()
                _myweb.implicitly_wait(self.timeoutImplicitlyWait)
                self.myCheckTitle(_myweb)
                i = i + 1
                #time.sleep(1)
            except Exception as e:
                try:
                    if TmpStockStatus == "僑外資":
                        TmpCorp     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[8]").get_attribute("innerHTML")
                        TmpAdd      = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[14]").get_attribute("innerHTML")
                        TmpName     = _myweb.find_element_by_xpath("(//table[@class='table table-striped']/tbody/tr/td)[12]").get_attribute("innerHTML")
                        TmpCorp     = TmpCorp[0:TmpCorp.index("<span")].strip()
                        TmpAdd      = TmpAdd[0:TmpAdd.index("<span")].strip()
                        TmpName     = TmpName.strip()
                    else:
                        print('Error! MyMoreLinkCollection1:' + str(i))
                        print(e)
                        self.tableMyError.append([str(DateTimeNow),self.myQryCond,self.myStartPage,self.myStopPage,self.myDataType,'Error! MyMoreLinkCollection1',TmpDataType,_PageCurrent,str(i)])
                    _myweb.back()
                    _myweb.implicitly_wait(self.timeoutImplicitlyWait)
                    self.myCheckTitle(_myweb)
                    i = i + 1
                    # quit()
                    continue
                except Exception as e:
                    print('Error! MyMoreLinkCollection2:' + str(i))
                    print(e)
                    self.tableMyError.append([str(DateTimeNow),self.myQryCond,self.myStartPage,self.myStopPage,self.myDataType,'Error! MyMoreLinkCollection2',TmpDataType,_PageCurrent,str(i)])
                    _myweb.back()
                    _myweb.implicitly_wait(self.timeoutImplicitlyWait)
                    self.myCheckTitle(_myweb)
                    i = i + 1
                    continue

    def myMainCrawler(self):
        try:
            DateTimeNow     = datetime.datetime.now()
            DateTimeNowFile = DateTimeNow
            DateTimeStart   = DateTimeNow
            DateTimeStop    = DateTimeNow
            if self.isDebugMode : print(DateTimeNow)
            mySessionID = DateTimeNow.microsecond

            ### Python操作Excel新版本xlsx文件 | 不懂真人 - https://goo.gl/K8M7Eg
            # 在内存中创建一个workbook对象，而且会至少创建一个 worksheet
            wb = Workbook()
            #获取当前活跃的worksheet,默认就是第一个worksheet
            ws = wb.active
            #可以使用append插入一行数据
            #ws.append(['頁次','筆次','公司','地址','負責人','抓取時間'])

            # Open the URL
            optionA = webdriver.ChromeOptions()
            optionA.add_argument('headless')
            optionA.add_argument("--disable-popup-blocking")

            optionB = webdriver.ChromeOptions()
            # optionB.add_argument('--disable-popup-blocking')
            chrome_prefs = {}
            optionB.experimental_options["prefs"] = chrome_prefs
            chrome_prefs["profile.default_content_settings"] = { "popups": 0 }

            if (self.myHeadlessMode == "1") :
                print('HeadLessMode = true')
                myweb = webdriver.Chrome(options=optionA)
            else :
                print('HeadLessMode = false')
                myweb = webdriver.Chrome(options=optionB)
            myweb.get('https://findbiz.nat.gov.tw/fts/query/QueryBar/queryInit.do')
            myweb.implicitly_wait(self.timeoutImplicitlyWait)

            # Popup
            # selenium.webdriver.ChromeOptions Python Example - https://goo.gl/2jnnUc
            # Selenium disable popup blocker in different browsers · Tech Adventures by Tarun Lalwani - https://goo.gl/vTpmH5 
            # Selenium Webdriver with Python - driver.title parameter - Stack Overflow - https://goo.gl/fhjtn4
            print('Browser Window Counts:' + str(len(myweb.window_handles)))
            i = 1
            while i < len(myweb.window_handles):
                myweb.switch_to.window(myweb.window_handles[i])
                myweb.close()
            myweb.switch_to.window(myweb.window_handles[0])
            myweb.implicitly_wait(self.timeoutImplicitlyWait)

            # Search Criteria Entrance
            myweb.find_element_by_id('qryCond').send_keys(self.myQryCond)
            myweb.find_element_by_id('infoAddr').click()
            
            if self.myDataType2 == "1": myweb.find_element_by_xpath("//input[@value='brCmpyType']").click()
            if self.myDataType3 == "1": myweb.find_element_by_xpath("//input[@value='busmType']").click()
            if self.myDataType4 == "1": myweb.find_element_by_xpath("//input[@value='factType']").click()
            if self.myDataType5 == "1": myweb.find_element_by_xpath("//input[@value='lmtdType']").click()
            if self.myDataType1 == "0": myweb.find_element_by_xpath("//input[@value='cmpyType']").click()

            myweb.find_element_by_id('isAliveY').click()
            myweb.find_element_by_id('qryBtn').click()

            # Get Search Result Stats
            DataRowsTotal = ""
            PageTotal     = ""
            PageCurrent   = ""
            PageTitle     = ""

            try:
                print("程式運行中，請等待 1 分鐘以上")
                print("請勿關閉程式......")
                DataRowsTotal = myweb.find_element_by_id('totalCount').get_attribute("value")
                PageTotal     = myweb.find_element_by_id('totalPage').get_attribute("value")
                PageCurrent   = myweb.find_element_by_id('currentPage').get_attribute("value")
            except Exception as e:
                print(e)
                print("程式正常，搜尋結果只有 1 頁.....")
                DataRowsTotal = myweb.find_element_by_xpath("(//*[@class='col-lg-12 col-md-12 col-sm-12 col-xs-12']/div)[7]").get_attribute("innerHTML")
                DataRowsTotal = DataRowsTotal[DataRowsTotal.index("共")+1:DataRowsTotal.index("筆")].strip()
                DataRowsTotal = DataRowsTotal.strip("</span>")
                PageTotal     = "1"
                PageCurrent   = "1"
                
            print("DataRowsTotal: " + DataRowsTotal)
            print("PageTotal: " + PageTotal)

            ws.append(['qryCond','搜尋資料','資料種類','登記現況','搜尋筆數','搜尋頁數','程式版本','網頁版本'])
            ws.append([self.myQryCond,'infoAddr',self.myDataType,'isAliveY',DataRowsTotal,PageTotal,self.myAppVersion,self.officialSiteVersion]) # 商工登記公示資料查詢服務 - https://goo.gl/D6onx3
            ws.append(['頁次','筆次','公司','地址','負責人','資料種類','抓取時間'])

            i = self.myStartPage
            while i < int(PageTotal)+1:
            # for i in range(myStartPage,int(PageTotal)+1,1):
                #if PageTitle == "錯誤":
                #    myweb.back()
                #    i = i - 1
                if int(PageTotal) > 1:
                    # mygotoPage = "gotoPage(" + str(i)+ ");" 
                    # element = myweb.find_element_by_xpath("//a[@onclick='" + mygotoPage + "']")
                    # myweb.execute_script("arguments[0].scrollIntoView();", element)
                    # element.click()
                    myweb.execute_script("gotoPage(" + str(i)+ ")")
                    myweb.implicitly_wait(self.timeoutImplicitlyWait)
                    # time.sleep(1)
                # Check Title
                elementTitle = myweb.find_element_by_tag_name("title")
                elementTitleHtml = elementTitle.get_attribute("innerHTML")
                PageTitle = elementTitleHtml
                print("官方網址版本: " + self.officialSiteVersion)
                print("本程式版本: " + self.myAppVersion)
                print("Search: " + self.myQryCond)
                print("PageTitle: " + PageTitle)
                if PageTitle == "錯誤":
                    time.sleep(10)
                    myweb.back()
                    continue
                # Go into detail
                if int(PageTotal) > 1:
                    PageCurrent   = myweb.find_element_by_id('currentPage').get_attribute("value")
                    print("PageTotal: " + PageTotal)
                    print("PageCurrent: " + PageCurrent)

                DateTimeNow = datetime.datetime.now()
                tableMylog = [[DateTimeNow,self.myAppVersion,str(mySessionID),self.myQryCond,self.myStartPage,self.myStopPage,self.myDataType,DataRowsTotal,PageTotal,PageCurrent]]
                self.MyMoreLinkCollection(wb, ws, myweb, PageCurrent)
                # MyMoreLinkCollection2(wb, ws, myweb, PageCurrent)
                #保存
                wb.save(filename="data/myCrawler2018_" + self.myQryCond + "_" + self.myDataType + "_" + str(mySessionID) + "_" + str(DateTimeNowFile.strftime("%Y%m%d%H%M%S")) + ".xlsx")
                with open('data/mylog_' + str(DateTimeNowFile.strftime("%Y%m")) + '.csv', 'a', newline='') as csvfile:
                    # 建立 CSV 檔寫入器
                    mylog = csv.writer(csvfile)
                    mylog.writerows(tableMylog)
                    mylog.writerows(self.tableMyError)
                self.tableMyError = []
                if self.myStopPage != 0 and i >= self.myStopPage : break
                elif i >= 499 : 
                    print ("Error! 搜尋結果大於 500 頁，請縮小搜尋範圍。")
                    break
                elif self.myStopPage >= 499 :
                    print ("Warning! 搜尋結果大於 500 頁，請縮小搜尋範圍。")
                i = i + 1    

            # Exit the app
            DateTimeStop  = datetime.datetime.now()
            if self.isDebugMode : print("Start: " + str(DateTimeStart))
            if self.isDebugMode : print("Stop: "  + str(DateTimeStop))
            if self.isDebugMode : print("Elapsed: " + str (DateTimeStop - DateTimeStart))
            # time.sleep(0)

            if self.isTurnOffChrome : myweb.quit()
        
        except Exception as e:
            print('Something wrong, please copy the following error message, and then contact Patrick.')
            print(e)

### Functions

def chkParameters():
    # Search Criteria
    print("Parameter Length: " + str(len(sys.argv)))

    if len(sys.argv) != 7: 
        print("Invalid parameters")
        quit()
    elif sys.argv[4].strip() == "00000":
        print("Invalid parameters: DataType")
        quit()

    print("arg1: "  + sys.argv[1])
    print("arg2: "  + sys.argv[2])
    print("arg3: "  + sys.argv[3])
    print("arg4: "  + sys.argv[4])
    print("arg41-cmpyType: " + sys.argv[4][0:1])
    print("arg42-brCmpyType: " + sys.argv[4][1:2])
    print("arg43-busmType: " + sys.argv[4][2:3])
    print("arg44-factType: " + sys.argv[4][3:4])
    print("arg45-lmtdType: " + sys.argv[4][4:5])
    print("arg5: "  + sys.argv[5])
    print("arg6: "  + sys.argv[6])

def getStreetName(self):
    print("test street name")
    url = 'https://www.post.gov.tw/post/internet/Postal/streetNameData_zip6.jsp'
    #values = {'city' : '臺北市','cityarea' : '信義區'}
    values = {'city' : '台北市','cityarea' : '信義區'}

    data = urllib.parse.urlencode(values)
    data = data.encode('UTF-8') # data should be bytes
    req = urllib.request.Request(url, data)
    the_page = ""
    
    with urllib.request.urlopen(req) as response:
        the_page = response.read()
    
    # the_page = the_page.decode('UTF-8',"ignore")
    # print (the_page)
    # mycode = "路"
    # mycode = mycode.encode('UTF-16BE')
    # print(mycode)
    # mycode = b'\x8d\xef'
    # mycode = mycode.decode('UTF-16BE')
    # print(mycode)
    
    soup = BeautifulSoup(the_page, 'html.parser')
    # print(soup.prettify())

    newDictionary=json.loads(str(soup))
    print(type(newDictionary))
    print(newDictionary)
    print(newDictionary[0])
    for myDict in newDictionary:
        print(myDict.get('street_name'))


### Main
def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        print('start')

        # getStreetName()

        chkParameters()

        myObj = myselenium2()

        myObj.myQryCond       = sys.argv[1].strip()
        myObj.myStartPage     = int(sys.argv[2])
        myObj.myStopPage      = int(sys.argv[3]) # 0 means all
        myObj.myDataType      = sys.argv[4]
        myObj.myDataType1     = sys.argv[4][0:1]
        myObj.myDataType2     = sys.argv[4][1:2]
        myObj.myDataType3     = sys.argv[4][2:3]
        myObj.myDataType4     = sys.argv[4][3:4]
        myObj.myDataType5     = sys.argv[4][4:5]

        myObj.myTurnOffChrome = sys.argv[5]
        myObj.myHeadlessMode  = sys.argv[6]

        myObj.mySendMailUsage()
        myObj.myMainCrawler()

    except Exception as e:
        print('fail')
        print(e)

    quit()

# - [Python之父教你写main()函数 - 精品 IT 资源分享](https://gti.page.link/iVNrm1zXqqDJSHMN9)
if __name__ == "__main__":
    main()

'''Test
python3 myselenium2.py $mykeyword $mypagestart $mypagestop $mydatatype 0 1
python3 myselenium2.py 台北市內湖區 1 2 10000 1 0
'''

'''
### myAppVersion = "2020043001"
* Refactor main()
* Refactor myselenium2 with Class
* Add myselenium2starter
* Use city and city area to get street list from Chian Post
* Add "外國公司辦事處登記基本資料"
* officailSiteVersion = "1.3.6"

### myAppVersion = "2020010802"
* officialSiteVersion = "1.3.5"

### myAppVersion = "2020010801"
* Modify README.md

### myAppVersion = "2018113005"
### myAppVersion = "2018113004"
### myAppVersion = "2018113003"
### myAppVersion = "2018113002"
* Add TmpDataType == "外國公司登記基本資料"
* Branch develop
* Pull request and merge

### myAppVersion = "2018113001"
* Use 'conda' as python virtual environment

### myAppVersion = "2018111902"
* Try Catch 使用 Python 寄發 Gmail

### myAppVersion = "2018111503"
* Use command "caffeinate" to prevent macos sleeping mode while running.

### myAppVersion = "2018111502"
* Modify "TmpCorpType" fields from 7 to 9

### myAppVersion = "2018111501"
* Bug fix for count initial popup browser windows

### myAppVersion = "2018111401"
* Send email login notification with MacOS SN and application parameters

### myAppVersion = "2018111301"
* Close first Popup Page
* Modify queryCmpyDetail Fields
* officialSiteVersion = "1.3.1" # 20181113

### myAppVersion = "2018110901"
* Modify README.md

### myAppVersion = "2018110701"
* Use python3 directly in mycrawlerrun.sh instead of python

### myAppVersion = "2018110601"
* Add headless option

### myAppVersion = "2018103101"
* Add features: Auto Update

### myAppVersion = "2018102701"
* Release to GitHub

### myAppVersion = "2018102401"
* execute script
* Add myAppVersion
* Change 資料種類 field in the excel data
* Add '程式版本','網頁版本' in the excel data
'''

# example: python myselenium2.py 宜蘭 1 2 00010
# # quit()

# AES-demo
# python3.6 实现AES加密、解密（改版） - melody_sy博客 - CSDN博客 - https://goo.gl/75cDTv

#driver = webdriver.Chrome()
#driver.get("http://www.baidu.com")
#driver.find_element_by_id('kw').send_keys('selenium')
#driver.find_element_by_id('su').click()
#driver.quit()

# print('mytest')
# quit()

# [Python] 使用Selenium在Google Chrome瀏覽器 @ Jialin :: 痞客邦 :: - https://goo.gl/TTv8C8
#web = webdriver.Chrome()
#web.get('http://www.cwb.gov.tw/V7/')
#web.set_window_position(0,0) #瀏覽器位置
#web.set_window_size(700,700) #瀏覽器大小
#time.sleep(5)
#web.find_element_by_link_text('天氣預報').click() #點擊頁面上"天氣預報"的連結
#time.sleep(5)
#web.close()

# Upload Google Drive
# Python & Google Drive 專案 — 2 – yysu – Medium - https://goo.gl/hGhEAu
# 利用 PyDrive 實現自動Google硬碟備份 @ kuohfjack的部落格 :: 痞客邦 :: - https://goo.gl/xPNbgd
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# gauth = GoogleAuth()
# gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
# drive = GoogleDrive(gauth)
# try:
#     name = '/Users/patrick/mycrawler/data/mylog.csv'  # It's the file which you'll upload
#     file = drive.CreateFile()  # Create GoogleDriveFile instance
#     file.SetContentFile(name)
#     file.Upload()
# except :
#     print("Unexpected error:", sys.exc_info()[0])
# quit()

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

'''
Reference:
4. 查找元素 — Selenium-Python中文文档 2 documentation - https://goo.gl/6yKn8g
Python String List Examples - Dot Net Perls - https://goo.gl/gb3Gjx
selenium-python-常用方法集锦（持续不断补充） - 程序园 - https://goo.gl/iCpob7
Python selenium —— 一定要会用selenium的等待，三种等待方式解读 « 灰蓝 - https://goo.gl/gUz7QL
网页处理实践（3）——python+selenium+firefox，不弹出窗口，静默模式运行 - qq_28053189的博客 - CSDN博客 - https://goo.gl/t1rGqu
Python & Google Drive 專案 — 2 – yysu – Medium - https://goo.gl/hGhEAu
pip - Managing contents of requirements.txt for a Python virtual environment - Stack Overflow - https://goo.gl/8zo2Y9
Jupyter Notebook 快速入门（上）| 编程派 | Coding Python - https://goo.gl/A93CS9
Python - selenium自動化-Chrome(headless) - 掃文資訊 - https://goo.gl/ndz75H
Python to print out status bar and percentage - Stack Overflow - https://goo.gl/xym4mV
'''