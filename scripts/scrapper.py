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

users = []
user_type = []
user_msg = []
user_messages_count = []
user_location = []


driver.get("https://www.mentalhealthforum.net/forum/forums/anxiety-forum.365/")

thread_container = driver.find_element("xpath", "//div[contains(@class,'structItemContainer-group js-threadList')]")
titles = thread_container.find_elements("xpath", ".//div[contains(@class, 'structItem-title')]")
links = []
for title in titles:
    link = title.find_element("xpath", ".//a[contains(@href, 'thread')]")
    links.append(link.get_attribute("href"))
    # driver.execute_script("arguments[0].click();", link)
    # time.sleep(15)
for link in links:
    driver.get(link)
    soup = BeautifulSoup(driver.page_source,"html.parser")
    name = driver.find_element("xpath", ".//span[contains(@class, 'username')]")
    
    time.sleep(1)



    



# print(link.get_attribute("href"))
# time.sleep(2)
# link.click()

# for thread in threads:
#     thread.find_element(By.XPATH, "//a[@href]")
# html = driver.page_source
# soup = BeautifulSoup(html,"html.parser")
# threads = soup.find_all("div", class_="structItemContainer-group")
# soup = BeautifulSoup(threads,"html.parser")


