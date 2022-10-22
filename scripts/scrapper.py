from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time



options = Options()
options.add_argument("--disable-infobars")
options.add_argument("start-maximized")
options.add_argument("--disable-extensions")
options.add_experimental_option("detach", True)



driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()

driver.get("https://www.mentalhealthforum.net/forum/forums/anxiety-forum.365/")

thread_container = driver.find_element("xpath", "//div[contains(@class,'structItemContainer-group js-threadList')]")
time.sleep(1)
titles = thread_container.find_elements("xpath", ".//div[contains(@class, 'structItem-title')]")
for title in titles:
    link = title.find_element("xpath", ".//a[contains(@href, 'thread')]")
    time.sleep(10)
    link.click()
    # print(link.get_attribute("href"))
    



# print(link.get_attribute("href"))
# time.sleep(2)
# link.click()

# for thread in threads:
#     thread.find_element(By.XPATH, "//a[@href]")
# html = driver.page_source
# soup = BeautifulSoup(html,"html.parser")
# threads = soup.find_all("div", class_="structItemContainer-group")
# soup = BeautifulSoup(threads,"html.parser")


