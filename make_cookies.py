from selenium.webdriver import Firefox
import pickle
from multiprocessing import freeze_support


if __name__ == '__main__':
    browser = Firefox()
    freeze_support()
    try:
        browser.get("https://aviso.bz/")
        final = input('press any key')
    finally:
        pickle.dump(browser.get_cookies(), open("cookie", "wb"))
        browser.close()
        browser.quit()
