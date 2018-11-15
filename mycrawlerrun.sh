#!/bin/bash
cd ~/findbiz/myCrawler2018-master
# source bin/activate
# source venv.sh
# pip install -r requirements.txt
pwd
python --version
pip --version
python3 --version
pip3 --version


echo "請輸入關鍵字(中文地區名)："
read mykeyword
echo "請輸入開始頁數(數字，最少請輸入 1)："
read mypagestart
echo "請輸入結束頁數(數字，0 為全部)："
read mypagestop
echo "資料種類有5種，輸入方式為5個位元，例：10000"
echo "分別為「公司」、「分公司」、「商業」、「工廠」、「有限合夥」"
echo "若欲查詢的資料種類為「公司」，請輸入：10000"
echo "若欲查詢的資料種類為「商業」，請輸入：00100"
echo "若欲查詢的資料種類為「公司」或「商業」，請輸入：10100"
echo "以上，如此類推"
echo "請輸入資料種類(5個位元，例：10000)："
read mydatatype
echo "Please wait..."

# pip install selenium
# pip install openpyxl
# python myselenium2.py 台中市北區 1 1 10000 0
# Quick Tip: caffeinate your Terminal - BrettTerpstra.com - https://goo.gl/sXvwRh
caffeinate -i python3 myselenium2.py $mykeyword $mypagestart $mypagestop $mydatatype 0 1

open ~/findbiz/myCrawler2018-master/data/
exit
# deactivate