import time
import os
import re
import PIL
import selenium
from tqdm import tqdm
import qrcode
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

options = Options()
options.set_headless(True)
driver = webdriver.Firefox(options=options, executable_path=r'geckodriver.exe')
driver.get('http://web.whatsapp.com')
driver.set_window_size(1400,900)
time.sleep(1)

token = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div').get_attribute('data-ref')
img = qrcode.make(token)
size = 300,300
img.thumbnail(size, PIL.Image.ANTIALIAS)
img.show()
time.sleep(6)
img.close()

try:
    num = int(input('\nenter number of people you want to send the text to : '))
    msg = input('enter the message : ')
    no = []
    for i in range(1,num+1):
        while True:
            tmp = i%10
            try:
                if tmp == 1:
                    x = int(input('\nenter '+str(i)+'st number : '))
                elif tmp == 2:
                    x = int(input('enter '+str(i)+'nd number : '))
                elif tmp == 3:
                    x = int(input('enter '+str(i)+'rd number : '))
                else:
                    x = int(input('enter '+str(i)+'th number : '))
                pat = re.compile(r'^[0-9]\d{9}$')
                p = re.findall(pat,str(x))
                if p:
                    no.append(x)
                    break
                else:
                    print('pattern dosent match !')
            except ValueError:
                print('Invalid Input ! ')
                continue       
except ValueError:
    print('Invalid Input ! ')

for i in tqdm(range(0,num)):
    elm = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[1]')
    driver.execute_script("arguments['0'].innerHTML = '<a href=\"https://api.whatsapp.com/send?phone="+"+91"+str(no[i])+"&message="+msg+"id=\"contact"+str(i+1)+">"+str(i+1)+"</a>';", elm)

    msgele = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[3]/div/div[1]/a")
    msgele.click()
    time.sleep(1)
    focus = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
    focus.send_keys(msg)
    focus.send_keys(Keys.ENTER)
    

print('done')
time.sleep(1)
dot = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/header/div[2]/div/span/div[3]/div')
dot.click()
time.sleep(1)
logout = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/header/div[2]/div/span/div[3]/span/div/ul/li[6]/div')
logout.click()
print('logged out')

if os.path.exists('QRcode.png'):
    os.remove('QRcode.png')


driver.quit()
