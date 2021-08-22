from selenium.webdriver.common.keys import Keys
import pytz
import time
from datetime import datetime

# system libraries
import os
import urllib

# recaptcha libraries
import pydub
import speech_recognition as sr

def runscript(email, password, browser):

    try:
        try:
            browser.get("https://siswa.smktelkom-mlg.sch.id").set_page_load_timeout(60)
        except:
            browser.close()
            return False

        emailinput = browser.find_element_by_xpath(
            '//*[@id="form_login"]/div[2]/div/input')
        passinput = browser.find_element_by_xpath(
            '//*[@id="form_login"]/div[3]/div/input')

        enter = browser.find_element_by_id('masuk')

        emailinput.send_keys(str(email))
        passinput.send_keys(str(password))

        captcha(browser, Keys)
        # time.sleep(25)

        enter.click()
    except:
        return False

    time.sleep(2)

    browser.get("https://siswa.smktelkom-mlg.sch.id/presnow")

    print("[INFO] Waiting time 06:00AM WIB")
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
    inputabsen = browser.find_element_by_xpath(
        "/html/body/section[2]/div[2]/div[2]/form/div/div[2]/div[1]/label[1]")
    simpan = browser.find_element_by_id("simpan")
    inputabsen.click()
    simpan.click()


def cek_absen(browser):
    tmp = browser.find_element_by_class_name('number')
    if(tmp.text == 'Masuk'):
        return True
    else:
        return False


def logout(browser):
    browser.get("https://siswa.smktelkom-mlg.sch.id/login/logout")
    browser.close()


def override(email, password, browser):
    while True:
        data = runscript(email, password, browser)
        if data == True:
            return True

def captcha(browser, Keys):
    # main program
    # switch to recaptcha frame
    frames = browser.find_elements_by_tag_name("iframe")
    browser.switch_to.frame(frames[0])
    browser.implicitly_wait(5)

    # click on checkbox to activate recaptcha
    browser.find_element_by_class_name("recaptcha-checkbox-border").click()

    try:
        # switch to recaptcha audio control frame
        browser.switch_to.default_content()
        frames = browser.find_element_by_xpath("/html/body/div[2]/div[4]").find_elements_by_tag_name("iframe")
        browser.switch_to.frame(frames[0])
        browser.implicitly_wait(5)

        # click on audio challenge
        browser.find_element_by_id("recaptcha-audio-button").click()

        # switch to recaptcha audio challenge frame
        browser.switch_to.default_content()
        frames = browser.find_elements_by_tag_name("iframe")
        browser.switch_to.frame(frames[-1])
        browser.implicitly_wait(5)

        audioRecognition(browser, Keys)
        
        count = 0
        multiple_correct = browser.find_elements_by_class_name("rc-audiochallenge-error-message")
        while(multiple_correct):
            audioRecognition(browser, Keys)
            multiple_correct = browser.find_elements_by_class_name("rc-audiochallenge-error-message")
            count += 1
            if(count == 3): 
                break
    except Exception:
        print("[INFO] Aduuuh keblokir ngab, balen maneng")
    
    browser.switch_to.default_content()
    browser.implicitly_wait(5)


def audioRecognition(browser, Keys):
    # get the mp3 audio file
    src = browser.find_element_by_id("audio-source").get_attribute("src")
    print("[INFO] Audio src: %s" % src)

    # download the mp3 audio file from the source
    urllib.request.urlretrieve(src, os.path.normpath(os.getcwd() + "\\sample.mp3"))
    browser.implicitly_wait(5)

    # load downloaded mp3 audio file as .wav
    try:
        sound = pydub.AudioSegment.from_mp3(os.path.normpath(os.getcwd() + "\\sample.mp3"))
        sound.export(os.path.normpath(os.getcwd() + "\\sample.wav"), format="wav")
        sample_audio = sr.AudioFile(os.path.normpath(os.getcwd() + "\\sample.wav"))
    except Exception:
        print("[ERR] Please run program as administrator or download ffmpeg manually, "
                "http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/")

    # translate audio to text with google voice recognition
    r = sr.Recognizer()
    with sample_audio as source:
        audio = r.record(source)
    key = r.recognize_google(audio)
    print("[INFO] Recaptcha Passcode: %s" % key)

    # key in results and submit

    browser.find_element_by_id("audio-response").send_keys(key.lower())

    browser.find_element_by_id("audio-response").send_keys(Keys.ENTER)