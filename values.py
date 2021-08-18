import os
from selenium import webdriver
from selenium.webdriver.common import proxy
from selenium.webdriver.common.proxy import Proxy, ProxyType
from randomproxy import Random_Proxy
import json
#
#
#
# Emailmu Si AKAD blyat
Email = "gagas_surya_28rpl@student.smktelkom-mlg.sch.id"
#
#
#
# Passwordmu Si AKAD blyat
Password = "Sealyichinaisha"


def email():
    return Email


def password():
    return Password

def browser():

    print("Ngambil proxy dulu ngab...")

    proxy_ip_port = ambilProxy()
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = proxy_ip_port
    proxy.ssl_proxy = proxy_ip_port

    cap = webdriver.DesiredCapabilities.CHROME
    proxy.add_to_capabilities(cap)

    print(f"Dapet nih: {proxy_ip_port}")

    chromes = webdriver.ChromeOptions()
    chromes.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # chromes.add_argument("--headless")
    # chromes.add_argument("--no-sandbox")
    chromes.add_argument("--disable-dev-sh-usage")

    ## Release
    # webdriver for heroku
    # browser = webdriver.Chrome(executable_path=os.environ.get(
    #     "CHROMEDRIVER_PATH"), chrome_options=chromes)
    
    ## Development
    browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=chromes, desired_capabilities=cap)
    
    return browser

def ambilProxy():
    proxy = Random_Proxy()

    url = 'https://siswa.smktelkom-mlg.sch.id'
    request_type = "post"

    # Using Proxy {'https': '34.138.225.120:8888'}
    r = proxy.Proxy_Request(url=url, request_type=request_type)
    parseproxy = json.loads(json.dumps(r))
    return parseproxy["https"]