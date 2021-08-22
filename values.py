import os
from selenium import webdriver
from fake_useragent import UserAgent

# change useragent
useragent = UserAgent()

# Login Account
# Email = os.environ.get("EMAIL")
# Password = os.environ.get("PASSWORD")
# Website logger
Website_url = "https://siswa.smktelkom-mlg.sch.id"
Website_url_absen = "https://siswa.smktelkom-mlg.sch.id/presnow"
Website_key = "6Lc7NmoUAAAAAJAgPU2_TypLL0H1UG_Fj9vUMl3O"
Captcha_api = os.environ.get("API")

# =====================================
# DON'T CHANGE THIS SETUP!
# def account():
#     return Email, Password


# def password():
#     return Password

def browser():
    chromes = webdriver.ChromeOptions()
    chromes.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chromes.add_argument(f"user-agent={useragent.random}")
    chromes.add_argument("--headless")
    chromes.add_argument("--no-sandbox")
    chromes.add_argument("--disable-dev-sh-usage")

    ## Release
    # webdriver for heroku
    # browser = webdriver.Chrome(executable_path=os.environ.get(
    #     "CHROMEDRIVER_PATH"), chrome_options=chromes)
    
    ## Development
    browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')

    return browser