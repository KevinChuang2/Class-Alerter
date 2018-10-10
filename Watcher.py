from SMS import send_msg
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#gets class info from class planner
def class_is_open(driver, subj,catalog,lecture):
    driver.find_element_by_xpath('//*[@id="searchTier0"]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="searchTier0"]').send_keys(subj)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="searchTier0"]').send_keys(Keys.ENTER)
    time.sleep(6)
    driver.find_element_by_xpath('//*[@id="searchTier1"]').send_keys(catalog)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="searchTier1"]').send_keys(Keys.ENTER)
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="ctl00_MainContent_cs_goButton"]').click()
    time.sleep(5)
    class_info = driver.find_element_by_xpath('//*[@id="container_course_M0"]').text
    list_classes = class_info.splitlines()
    class_capacity = ''
    for x, line in enumerate(list_classes):
        if line == lecture:
            class_capacity = list_classes[x+1]
    if 'Open' in class_capacity:
        return True
    return False

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('window-size=1920,1080')
driver = webdriver.Chrome("C:\\Users\\Kevin\\Documents\\WaitlistTexter\\chromedriver.exe",chrome_options=chrome_options)
driver.set_page_load_timeout(30)
wait = WebDriverWait(driver,15)
user = 'kevinchuang'
gmail = 'kevinchuang2@gmail.com'
myucla = 'https://my.ucla.edu/'
driver.get(myucla)
subj = 'LIFESCI'
catalog = '7C'
lecture = 'Lec 3'
subj2 = 'Psychology'
catalog2 = '100a'
lecture2 = 'Lec 2'
#click sign in link, type in login and password
driver.find_element_by_xpath('//*[@id="ctl00_signInLink"]').click()
driver.find_element_by_xpath('//*[@id="logon"]').send_keys(user)
driver.find_element_by_xpath('//*[@id="pass"]').send_keys(password)
driver.find_element_by_xpath('//*[@id="sso"]/div/button').click()

#needs to switch to duo iframe
driver.switch_to.frame("duo_iframe")

#look for 2nd device because I don't want to get spammed
devices = driver.find_element_by_name('device')
for option in devices.find_elements_by_tag_name('option'):
    if option.text == 'Mobile (XXX-XXX-3094)':
        option.click()

options = driver.find_element_by_xpath('//*[@id="login-form"]/fieldset[3]')
driver.find_element_by_xpath('//*[@id="login-form"]/fieldset[3]/div[2]')
hidden = driver.find_element_by_xpath('//*[@id="login-form"]/fieldset[3]/div[2]')
action = ActionChains(driver)
#click the passcode form
action.move_to_element_with_offset(hidden,300,40).click().perform()
driver.find_element_by_xpath('//*[@id="message"]').click()

duo_code_driver=webdriver.Chrome("C:\\Users\\Kevin\\Documents\\WaitlistTexter\\chromedriver.exe")
duo_code_driver.set_page_load_timeout(5)
duo_wait = WebDriverWait(duo_code_driver,10)

duo_action = ActionChains(duo_code_driver)
duo_code_driver.get('https://voice.google.com/about')
duo_code_driver.find_element_by_xpath('//*[@id="header"]/div[2]/a').click()
time.sleep(2)
duo_code_driver.find_element_by_xpath('//*[@id="identifierId"]').send_keys(gmail)
duo_code_driver.find_element_by_xpath('//*[@id="identifierNext"]/content/span').click()
time.sleep(2)
duo_wait.until(EC.presence_of_element_located((By.ID, 'password')))
duo_code_driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(gmail_pwd)
duo_code_driver.find_element_by_xpath('//*[@id="passwordNext"]/content/span').click()
time.sleep(7)

elem=duo_code_driver.find_element_by_xpath('//*[@id="messaging-view"]/div/div/md-content/div')
sms_code = elem.text.splitlines()[4].split(' ')[2]
duo_code_driver.close()

driver.find_element_by_xpath('//*[@id="login-form"]/fieldset[3]/div[2]/input[2]').send_keys(sms_code)
driver.find_element_by_xpath('//*[@id="login-form"]/fieldset[3]/div[2]/input[2]').send_keys(Keys.ENTER)
time.sleep(2)

driver.get('https://be.my.ucla.edu/ClassPlanner/ClassPlan.aspx')
eud_msg = ''
kev_msg = ''
if class_is_open(driver, subj, catalog, lecture):
    kev_msg += 'EMPTY: ' + subj + ' ' + catalog + ' ' + lecture + ' \t'
    #send_msg('kevinchuang2@gmail.com', 'yo ' + subj + ' ' + catalog + ' ' + lecture+ ' is empty')
else:
    kev_msg +='FULL: ' + subj + ' ' + catalog + ' ' + lecture + ' \t'


if class_is_open(driver, subj2, catalog2, lecture2):
    kev_msg += 'EMPTY: ' + subj2 + ' ' + catalog2 + ' ' + lecture2
else:
    kev_msg += 'FULL: ' + subj2 + ' ' + catalog2 + ' ' + lecture2

send_msg('kevinchuang2@gmail.com', kev_msg)

driver.close()

