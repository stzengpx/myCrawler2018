#!/bin/bash
printf "請輸入帳號:"
read Name
echo "您的帳號是：$Name"
if [[ $1 == "update" ]];then
    echo "Updating......"
    rm master.zi*
    wget https://github.com/stzengpx/myCrawler2018/archive/chinapost.zip
    unzip -oq master.zip
    cp myCrawler2018-chinapost/mycrawler.sh ~/findbiz/
    cp myCrawler2018-chinapost/mycrawlerrun.sh ~/findbiz/
    echo "Update Complete!"
fi
rm master.zi*
cd ~/findbiz/; bash mycrawlerrun_dev.sh