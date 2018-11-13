# MyCrawler

自動抓取 "商工登記公示資料查詢服務 - https://findbiz.nat.gov.tw/fts/query/QueryBar/queryInit.do" 資料，然後再輸出成 Excel 的表格檔案。

## Getting Started

以下將簡述開發相關套件及程式執行方式

### Prerequisites

#### 硬體
* MacBook Pro 15 Early 2011
* 2.0GHz 四核心 Intel Core i7
* 8GB 1333MHz DDR3 SDRAM
* 256GB 固態磁碟

#### 軟體
* macOS 10.13 High Sierra
* Google Chrome 版本 70.0.3538.67 (正式版本) (64 位元)
* Visual Studio Code 版本 1.28.2（1.28.2）
* [iTerm2](https://medium.com/statementdog-engineering/prettify-your-zsh-command-line-prompt-3ca2acc967f)
* 本程式為 Consol Application written in Python 

### Installing

A step by step series of examples that tell you how to get a development env running

The step will be...
1. brew

[macOS 缺少套件的管理工具 — macOS 缺少套件的管理工](https://goo.gl/rtR1Jd)
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```   
2. git
```
brew install git
```
3. wget
```
brew install wget
```
4. python
```
brew install python
```
5. pip
```
easy_install pip
```
6. virtualenv
* Install
```
pip install virtualenv
```
* Run
```
virtualenv -p python3 venv
```
7. openpyxl
```
pip install openpyxl
```
8. Selenium
```
pip install selenium
```
9.  Selenium WebDriver - ChromeDriver 2.43
[Selenium ChromeDriver - WebDriver for Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads)

#### (optional) Install all the packages for developing the project
```
pip freeze > requirements.txt # only for the really creator of this project
pip install pur
pip install -r requirements.txt
```

## Running the application for developers

執行終端機後，先切換至此 APP 的工作目錄，並進入 virtualenv。
```
cd mycrawler; source bin/activate; clear;
```
程式執行的指令格式如下：
```
python myselenium2.py [Arg1] [Arg2] [Arg3] [Arg4] [Arg5] [Arg6]
```
* Arg1: 文字；輸入地址區域關鍵字查詢字串
* Arg2: 數字；輸入啟始頁數，請輸入阿拉伯數字。最少請輸入 1
* Arg3: 數字；輸入結束頁數，請輸入阿拉伯數字。0 表示最後一頁；因目標網頁的限制，無法查看超過 500 頁的資料，故此參數最大值預設為498。
* Arg4: 數字(5 Bits)；輸入資料種類；請輸入5個bits，例如：10100 (1表示勾選；2表示不選)
    * Bit1 (最左邊): 公司 
    * Bit2: 分公司
    * Bit3: 商業
    * Bit4: 工廠
    * Bit5: 有限合夥
* Arg5: 數字；程式結束時，是否依然開著瀏覽器。1表示開著；0表式關閉。
* Arg6: 數字；是否採用 Chrome Headless Mode。1表示隱藏；0表式顯示 Chrome。

### Example:
```
python myselenium2.py 台中市北區 1 0 10000 0 1
```
## Running the application for users

### Prepare the environment
* Google Chrome 版本 70.0.3538.67 (正式版本) (64 位元) (以上)
* brew
* python 3
* virtualenv
* Selenium WebDriver - ChromeDriver 2.43
* wget

請下載-[操作手冊](https://goo.gl/QXufJV)

### Initial for the first run
```
clear
cd ~
mkdir findbiz
cd findbiz
wget https://github.com/stzengpx/myCrawler2018/archive/master.zip
unzip -oq master.zip
cp myCrawler2018-master/mycrawler.sh ~/findbiz/
```

### General running
#### Without update
```
clear; cd ~/findbiz; bash mycrawler.sh
```
#### With update
```
clear; cd ~/findbiz; bash mycrawler.sh update
```
#### Exception
Once there comes an error and the app down, you can force to stop it.
```
press [ctrl + c]
```
## Authors

* **Patrick Tseng** - *Initial work* - [stzengpx](https://github.com/stzengpx)

See also the list of [contributors](https://github.com/stzengpx/myCrawler2018/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* A template to make good README.md - https://goo.gl/tp2n6X

## Version

### myAppVersion = "2018111301"
* Close first Popup Page
* Modify queryCmpyDetail Fields
* officialSiteVersion = "1.3.1" # 20181113

### myAppVersion = "2018110901"
* Modify README.md
* Add Chrome Headless Mode

### myAppVersion = "2018103101"
* Add features: Auto Update

### myAppVersion = "2018102701"
* Release to GitHub

### myAppVersion = "2018102401"
* execute script
* Add myAppVersion
* Change 資料種類 field in the excel data
* Add '程式版本','網頁版本' in the excel data