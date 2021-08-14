import os
from selenium import webdriver
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
    chromes = webdriver.ChromeOptions()
    chromes.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chromes.add_argument("--headless")
    chromes.add_argument("--no-sandbox")
    chromes.add_argument("--disable-dev-sh-usage")

    ## Release
    # webdriver for heroku
    # browser = webdriver.Chrome(executable_path=os.environ.get(
    #     "CHROMEDRIVER_PATH"), chrome_options=chromes)
    
    ## Development
    browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=chromes)

    return browser