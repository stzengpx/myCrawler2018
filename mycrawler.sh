#!/bin/bash
printf "請輸入帳號:"
read Name
echo "您的帳號是：$Name"
if [[ $1 == "update" ]];then
    echo "Updating......"
    rm master.zi*
    wget https://github.com/stzengpx/myCrawler2018/archive/master.zip
    unzip -oq master.zip
    cp myCrawler2018-master/mycrawler.sh ~/findbiz/
    cp myCrawler2018-master/mycrawlerrun.sh ~/findbiz/
    echo "Update Complete!"
fi
rm master.zi*
cd ~/findbiz/; bash mycrawlerrun.sh