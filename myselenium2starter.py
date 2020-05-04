import myselenium2
import sys
import urllib.parse
import urllib.request
import json
from bs4 import BeautifulSoup

### Functions

def chkParameters():
    # Search Criteria
    print("Parameter Length: " + str(len(sys.argv)))

    if len(sys.argv) != 8: 
        print("Invalid parameters")
        quit()
    elif sys.argv[5].strip() == "00000":
        print("Invalid parameters: DataType")
        quit()

    print("arg1: "  + sys.argv[1])
    print("arg2: "  + sys.argv[2])
    print("arg3: "  + sys.argv[3])
    print("arg4: "  + sys.argv[4])
    print("arg5: "  + sys.argv[5])
    print("arg51-cmpyType: "   + sys.argv[5][0:1])
    print("arg52-brCmpyType: " + sys.argv[5][1:2])
    print("arg53-busmType: "   + sys.argv[5][2:3])
    print("arg54-factType: "   + sys.argv[5][3:4])
    print("arg55-lmtdType: "   + sys.argv[5][4:5])
    print("arg6: "  + sys.argv[6])
    print("arg7: "  + sys.argv[7])

def getStreetName(city, cityarea):
    city = city.replace("台","臺")
    try:
        url = 'https://www.post.gov.tw/post/internet/Postal/streetNameData_zip6.jsp'
        #values = {'city' : '臺北市','cityarea' : '信義區'}
        values = {'city' : city,'cityarea' : cityarea}

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

        newDictionary = json.loads(str(soup))
        
        return newDictionary
        # print(type(newDictionary))
        # print(newDictionary)
        # print(newDictionary[0])
        # for myDict in newDictionary:
        #     print(myDict.get('street_name'))
    
    except Exception as e:
        print('Get street name Err!')
        print(e)


### Main
def main():
    print("start")
    # python3 myselenium2starter.py 台北市 內湖區 1 2 10000 1 0
    # python3 myselenium2starter.py 000 台北市內湖區內湖路１段  1 2 10000 1 0

    myObj = myselenium2.myselenium2()
    myObj.mySendMailUsage()
    
    chkParameters()

    myObj.myStartPage     = int(sys.argv[3])
    myObj.myStopPage      = int(sys.argv[4]) # 0 means all
    myObj.myDataType      = sys.argv[5]
    myObj.myDataType1     = sys.argv[5][0:1]
    myObj.myDataType2     = sys.argv[5][1:2]
    myObj.myDataType3     = sys.argv[5][2:3]
    myObj.myDataType4     = sys.argv[5][3:4]
    myObj.myDataType5     = sys.argv[5][4:5]

    myObj.myTurnOffChrome = sys.argv[6]
    myObj.myHeadlessMode  = sys.argv[7]

    city = sys.argv[1].strip()
    cityarea = sys.argv[2].strip()

    if city == '000':
        myObj.myQryCond = cityarea
        myObj.myMainCrawler()
    
    else:

        myList = getStreetName(city,cityarea)

        if len(myList) == 0:
            print("Get street name fail!")
        else:
            myCondList = []

            for myDict in myList:
                myCondList.append(myDict.get('street_name'))
                # print(myDict.get('street_name'))

            for myStr in myCondList:
                # print(city+cityarea+myStr)
                myObj.myQryCond       = city + cityarea + myStr
                myObj.myMainCrawler()



if __name__ == "__main__":
    main()