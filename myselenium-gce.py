from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
opts = Options()
opts.add_argument('–headless') #無頭chrome
opts.add_argument('–disable-gpu')
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),chrome_options=opts)
driver.get('https://www.google.com/')
print(driver.title)
driver.close()

# https://www.maxlist.xyz/2019/04/14/selenium-chrome/
# 我是在 GCE 上使用 f1-micro 的機器，並選用 ubuntu 18.04 LTS 為 OS
# 在安裝 Chrome 瀏覽器時，還需要增加以下步驟：
# sudo apt-get update
# sudo apt-get upgrade
# sudo apt-get install chromium-driver
# wget -c https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# sudo dpkg -i google-chrome-stable_current_amd64.deb
# sudo apt-get install
# sudo apt-get install -f

# 然後 pythone 程式碼修改成上面那樣：