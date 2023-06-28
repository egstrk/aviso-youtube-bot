
#from config import name, password
import time
import pickle
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

option = Options()
option.add_argument("--disable-notifications")
#ioption.add_argument('--headless')
option.set_preference("media.volume_scale", "0.0")
option.add_argument("--mute-audio") 
browser = Firefox(options=option)
wait = WebDriverWait(browser, 15)


def aviso_sign_in():
    browser.get("https://aviso.bz/")
    for cookie in pickle.load(open('cookie', "rb")):
        browser.add_cookie(cookie)
    browser.refresh()
    time.sleep(5)
    button = wait.until(EC.element_to_be_clickable((By.ID, "mnu_title1")))
    button.click()
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'YouTube')]")))
    #browser.execute_script("arguments[0].click();", button)
    button.click()
    time.sleep(4)

YOUTUBE_VIEW = "ybprosm"
YOUTUBE_LIKE = "yblkvel"
YOUTUBE_SUBSCRIBE = "ybrvel"

class BuxTask:

    def __init__(self, element):
        self.corner         = element
        self.type           = self.__get_type()
        self.id             = self.__get_id()
        self.link           = self.__get_link()
        self.url            = self.__get_url()
        self.time           = self.__get_time()
        self.views_number   = self.__get_views_number()
        self.cost           = self.__get_cost()
        self.start_button   = {}
    
    def __get_id(self):
        if self.type == YOUTUBE_VIEW:
            prefix = "ads-link-"
        elif self.type == YOUTUBE_LIKE:
            prefix = "likes-link-"
        elif self.type == YOUTUBE_SUBSCRIBE:
            prefix = "podp-link-"
        return self.corner.get_attribute("id").replace(prefix, "")

    def __get_type(self):
        type_ = self.corner.find_element(By.XPATH, ".//div[contains(@class, 'yb')]").get_attribute("class")
        return type_

    def __get_link(self):
        if self.type == YOUTUBE_VIEW:
            prefix = "start-ads-"
        elif self.type == YOUTUBE_LIKE:
            prefix = "start-likes-"
        elif self.type == YOUTUBE_SUBSCRIBE:
            prefix = "start-podp-"
        container = browser.find_element(By.ID, prefix + self.id)
        return container.find_element(By.XPATH, ".//child::span[1]")

    def __get_url(self):
        if self.type == YOUTUBE_SUBSCRIBE:
            return ""
        return self.link.get_attribute("title")

    def __get_views_number(self):
        try:
            visits = self.corner.find_element(By.XPATH, ".//span[contains(@title, 'Осталось ')]").text
        except:
            visits = "99999"
        visits = visits.strip("()")
        return int(visits)

    def __get_cost(self):
        cost_string = self.corner.find_element(By.XPATH, ".//span[contains(@title, 'Стоимость')]").text[:-1]
        return round(float(cost_string), 3)

    def __get_time(self):
        if self.type == "ybprosm":
            time_string = self.corner.find_element(By.XPATH, ".//div[@style='margin-top:5px;']//child::span[1]").text.replace("сек", "").strip()
        else:
            time_string = "0"
        return int(time_string)

    def print_(self):
        print(f"{self.id}\t{self.type}\t{self.cost}\t{self.views_number}\t{self.time}\t{self.url}")

    def activate(self) -> bool:
        browser.execute_script("arguments[0].click();", self.link)
        try:
            start_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "go-link-youtube")))
        except:
            return False
        start_button.click()
        try:
            wait.until(EC.number_of_windows_to_be(2))
        except:
            return False
        browser.switch_to.window(browser.window_handles[1])
        return True

    def __close(self):
        browser.close()
        browser.switch_to.window(browser.window_handles[0])


    def hide(self):
        self.corner.find_element(By.XPATH, ".//a[contains(@title, 'Скрыть площадку')]").click()
        print("Task hidden")
        del self
            

def get_task_list():
    tasks = browser.find_elements(By.CLASS_NAME, "work-serf")

    task_list = []
    for task in tasks:
        new_task = BuxTask(task)
        task_list.append(new_task)
    return task_list

def start_video(expected_time) -> bool:

    try:
        wait.until(EC.presence_of_element_located((By.ID, "tmr")))
    except:
        return False
    tmr = browser.find_element(By.ID, "tmr")
    
    succes_error = browser.find_element(By.ID, "succes-error")

    wait.until(EC.presence_of_element_located((By.ID, "video-start")))
    wait.until(EC.element_to_be_clickable((By.ID, "video-start")))
    browser.switch_to.frame("video-start")
    
    try:
        button_play = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ytp-large-play-button")))
    except:
        print("Video unavailable")
        return False
    button_play.click()
    
    browser.switch_to.window(browser.window_handles[1])

    while tmr.text != "0":
        time.sleep(0.5)
   
    try:
        wait.until(EC.any_of(
            EC.text_to_be_present_in_element((By.ID, "succes-error"), "С учетом рефбека"),
            EC.text_to_be_present_in_element((By.ID, "succes-error"), "Ошибка")))
    except:
        browser.switch_to.frame("video-start")
        browser.find_element(By.CLASS_NAME, "ytp-large-play-button").click()
        browser.switch_to.window(browser.window_handles[1])
        wait.until(EC.text_to_be_present_in_element((By.ID, "succes-error"), "С учетом рефбека"))
        succes_error = browser.find_element(By.ID, "succes-error")

    if "Ошибка" in succes_error.text:
        return False

    return True

def close_video():
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
                                                        
aviso_sign_in()


total_earned = 0.0
total_rating = 0.0

while True:
    task_list = get_task_list()
    task_number = len(task_list)
    if task_number == 0:
        print("There's no any task. Sleeping for 15 minutes...")
        time.sleep(900)
    elif task_number > 1:
        task_list.sort(key = lambda x: x.views_number)
    for task in task_list:
        task.print_()
        if task.type == YOUTUBE_VIEW:
            if task.activate():
                if not start_video(task.time):
                    task.hide()
                    wait.until(EC.staleness_of(task.corner))
                close_video()
            else:
                task.hide()
                wait.until(EC.staleness_of(task.corner))
        else:
            task.hide()
            wait.until(EC.staleness_of(task.corner))
    browser.refresh()
    time.sleep(5)
browser.quit()
