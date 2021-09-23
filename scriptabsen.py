import pytz
import time
from datetime import datetime
from capmonster_python import NoCaptchaTaskProxyless
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert


def runscript(account, sitelogger, browser):
    try:
        print("Current session is {}".format(browser.session_id))
        browser.get(str(sitelogger[0]))
    except:
        browser.close()
        return False

    emailinput = browser.find_element_by_xpath(
        '//*[@id="form_login"]/div[2]/div/input')
    passinput = browser.find_element_by_xpath(
        '//*[@id="form_login"]/div[3]/div/input')
    enter = browser.find_element_by_id('masuk')

    emailinput.send_keys(str(account[0]))
    passinput.send_keys(str(account[1]))

    # skipcaptcha
    website_url = browser.current_url
    captcha = NoCaptchaTaskProxyless(client_key=str(sitelogger[2]))
    taskId = captcha.createTask(website_url, sitelogger[1])
    print("# Task created successfully, waiting for the response.")
    response = captcha.joinTaskResult(taskId)
    print("# Response received.")
    browser.execute_script(f"document.getElementsByClassName('g-recaptcha-response')[0].innerHTML = '{response}';")
    print(response)
    print("# Response injected to secret input.")

    time.sleep(5)
    enter.click()

    try:
        el = WebDriverWait(browser, timeout=5).until(lambda d: d.find_element_by_tag_name("h2"))
        assert el.text == "DASHBOARD"
    except:
        browser.close()
        return False

    browser.get(str(sitelogger[3]))

    print("# Nunggu jam 06:00AM WIB")
    while True:
        WIB = pytz.timezone('Asia/Jakarta')
        time_now = datetime.now(WIB)
        if time_now.strftime('%H') == '06' and time_now.strftime('%M') == '00':
            browser.refresh()
            if cek_absen(browser) == False:
                absen(browser)
                browser.refresh()
                if cek_absen(browser) == True:
                    logout(browser)
                    return True
                else:
                    logout(browser)
                    return False
            else:
                logout(browser)
                return True


def absen(browser):
    Masuk = browser.find_element_by_xpath(
        "/html/body/section[2]/div[2]/div[2]/form/div/div[2]/div[1]/div[2]/label[1]")
    Via = browser.find_element_by_xpath(
        "/html/body/section[2]/div[2]/div[2]/form/div/div[2]/div[2]/div[2]/label[1]")
    simpan = browser.find_element_by_id("simpan")
    Masuk.click()
    Via.click()
    simpan.click()
    # Alert
    alert = Alert(browser)
    alert.accept()


def cek_absen(browser):
    tmp = browser.find_element_by_class_name('number')
    if(tmp.text == 'Masuk'):
        return True
    else:
        return False


def logout(browser):
    browser.get("https://siswa.smktelkom-mlg.sch.id/login/logout")
    browser.close()


def override(account, sitelogger, browser):
    while True:
        data = runscript(account, sitelogger, browser)
        if data == True:
            return True