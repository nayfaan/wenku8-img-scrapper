# -*- coding: utf-8 -*-

import services.startDriver
import re
import urllib.request
import os
import pathlib
import traceback

from opencc import OpenCC

global ROOT_DIR
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
global OUTPUT
OUTPUT = os.path.join(ROOT_DIR, "output/")
pathlib.Path(OUTPUT).mkdir(parents=True, exist_ok=True)

global book_num

while True:
    print()
    book_num = input("Enter book ID: ")
    try:
        book_num = int(book_num)
    except:
        pass
    if type(book_num) is int:
        book_num = str(book_num)
        break
    
global start_from

while True:
    print()
    start_from = input("Start from index (first element is 0): ")
    try:
        start_from = int(start_from)
    except:
        pass
    if type(start_from) is int:
        break

def scrap(driver):
    cc = OpenCC('s2t')
    book_title = driver.find_element_by_id("title").get_attribute('innerHTML')
    book_title = cc.convert(book_title)
    
    table_obj = driver.find_element_by_css_selector("table.css")
    cells = table_obj.find_elements_by_tag_name("td")
    
    book_chapters = []
    for cell in cells:
        if cell.get_attribute('class') == "vcss":
            current_chapter = cell
            book_chapters.append({current_chapter: []})
        else:
            book_chapters[-1][current_chapter].append(cell)
            
    if start_from >= len(book_chapters):
        raise Exception("Error: start_from index higher than available chapter count.")
    else:
        book_chapters = book_chapters[start_from:]
            
    book_imgs = []
    for book in book_chapters:
        for chapter in list(book.values())[0]:
            if re.search('插图', chapter.get_attribute('innerHTML')):
                book_imgs.append({list(book.keys())[0].get_attribute('innerHTML'): "http://dl.wenku8.com/pack.php?aid="+book_num+"&vid="+re.findall("(?<=cid=)\d+", chapter.find_element_by_tag_name("a").get_attribute('href'))[0]})
    
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    
    for img_page in book_imgs:
        driver.get(list(img_page.values())[0])
        
        print()
        img_obj = driver.find_elements_by_css_selector(".chaptercontent a")
        img_list = list((o.get_attribute('innerText') for o in img_obj))
        
        current_title = list(img_page.keys())[0]
        
        IMG_FOLDER = os.path.join(OUTPUT, book_title + "（"+ current_title +"）/")
        pathlib.Path(IMG_FOLDER).mkdir(parents=True, exist_ok=True)
        
        for j in range(len(img_list)):
            file_ext = re.match(".*\.(.+)$", img_list[j])[1]
            urllib.request.urlretrieve(img_list[j], os.path.join(IMG_FOLDER, f"{j+1:02d}" + "." + file_ext))
            print("Retrieved: " + current_title + ": " + str(j+1))
    
def run():
    driver = services.startDriver.start()

    book_url = 'https://www.wenku8.net/modules/article/reader.php?aid='+book_num
    
    driver.get(book_url)
    
    try:
        scrap(driver)
    except:
        print(traceback.format_exc())
    finally:
        driver.close()

if __name__ == "__main__":
    print("\n")
    run()
