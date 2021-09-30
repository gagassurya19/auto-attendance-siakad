import pytz
import time
from datetime import datetime
from capmonster_python import NoCaptchaTaskProxyless
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def runscript(account, sitelogger, browser):
    try:
        print("\n")
        print("="*81)
        print("@ Current session is {}".format(browser.session_id))
        print("="*81)
        print("--- GoTo Login Page ---")
        browser.get(str(sitelogger[0]))
        browser.maximize_window()
    except:
        browser.close()
        return False

    emailinput = browser.find_element_by_css_selector("input[name=email]")
    passinput = browser.find_element_by_css_selector("input[name=password]")
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
    print("# Response injected to secret input.")

    time.sleep(5)
    enter.click()

    try:
        el = WebDriverWait(browser, timeout=5).until(lambda d: d.find_element_by_tag_name("h2"))
        assert el.text == "DASHBOARD"
    except:
        browser.close()
        return False

    print("--- Login Success ---")

    browser.get(str(sitelogger[3]))
    print("--- GoTo Absen Page ---")

    print("# Nunggu jam 06:00AM WIB")
    while True:
        WIB = pytz.timezone('Asia/Jakarta')
        time_now = datetime.now(WIB)
        if time_now.strftime('%H') == '06' and time_now.strftime('%M') == '00':
        # if True: # Development
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
    for i in range(10):
        try:
            #delete element with JavaScript Executor
            browser.execute_script("""
            var l = document.getElementsByClassName("page-loader-wrapper")[0];
            l.parentNode.removeChild(l);
            """)

            masuk = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH, ".//*[contains(text(), 'Masuk')]")))
            masuk.click()
            print("> MASUK")

            daring = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH, ".//*[contains(text(), 'DARING')]")))
            daring.click()
            print("> DARING")

            simpan = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH, ".//*[contains(text(), 'SIMPAN')]")))
            simpan.click()
            print("> SIMPAN")

            # Alert
            alert = browser.switch_to.alert
            alert.accept()
            print("> ACCEPT ALERT")
            break
        except NoSuchElementException as e:
            print('Retry in 1 second -{}'.format(i+1))
            time.sleep(1)


def cek_absen(browser):
    print("# Check Absen")
    tmp = browser.find_element_by_css_selector("div[class=number]")
    if(tmp.text == 'Masuk'):
        print("--- Absen Success ---")
        return True
    else:
        print("--- Absen Failed ---")
        return False


def logout(browser):
    print("--- Logout ---")
    print("="*81)
    browser.get("https://siswa.smktelkom-mlg.sch.id/login/logout")
    browser.close()