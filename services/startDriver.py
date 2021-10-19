from selenium import webdriver
from selenium import *

def start():
    return webdriver.Chrome(executable_path='./services/chromedriver')

if __name__ == "__main__":
    pass
