# -*- coding: utf-8 -*-

import services.startDriver
import re
import urllib.request
import os
import pathlib

global ROOT_DIR
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
global OUTPUT
OUTPUT = os.path.join(ROOT_DIR, "output/")
pathlib.Path(OUTPUT).mkdir(parents=True, exist_ok=True)

global book_num
book_num = "1829"

def scrap(driver):
    img_chp_obj = driver.find_elements_by_xpath("//*[contains(text(), '插图')]")
    img_url = list((o.get_attribute('href') for o in img_chp_obj))
    
    img_url = list(("http://dl.wenku8.com/pack.php?aid="+book_num+"&vid="+re.match("^.*?//.*?/.*?/.*?/.*?/([^\.]+)", u)[1] for u in img_url))
    
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    
    for i in range(len(img_url)):
        driver.get(img_url[i])
        img_obj = driver.find_elements_by_css_selector(".chaptercontent a")
        img_list = list((o.get_attribute('innerText') for o in img_obj))
        
        IMG_FOLDER = os.path.join(OUTPUT, "ぼくたちのリメイク（"+str(i+1)+"）/")
        pathlib.Path(IMG_FOLDER).mkdir(parents=True, exist_ok=True)
        
        for j in range(len(img_list)):
            file_ext = re.match(".*\.(.+)$", img_list[j])[1]
            urllib.request.urlretrieve(img_list[j], os.path.join(IMG_FOLDER, f"{j+1:02d}" + "." + file_ext))
            print("Retrieved: " + str(i+1) + "." + str(j+1))
    
def run():
    driver = services.startDriver.start()

    book_url = 'https://www.wenku8.net/novel/2/'+book_num+'/index.htm'
    
    driver.get(book_url)
    scrap(driver)
    try:
        pass
    except:
        pass
    finally:
        driver.close()

if __name__ == "__main__":
    print("\n")
    run()
