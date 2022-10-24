from email.mime import base
from msilib.schema import Error
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd



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
user_msg_count = []

inital_link = "https://www.mentalhealthforum.net/forum/forums/anxiety-forum.365/"

driver.get(inital_link)

# Returns max page number of forum
max_page_label = driver.find_elements("xpath", "//li[contains(@class,'pageNav-page')]")[-1]
forum_max_page = max_page_label.find_element("xpath", ".//a[@href]").text


for i in range(1, int(3), 1):
    page_num = f"/page-{i}"
    driver.get(inital_link + page_num)
    # Returns all links of the page in a list called links
    thread_container = driver.find_element("xpath", "//div[contains(@class,'structItemContainer-group js-threadList')]")
    titles = thread_container.find_elements("xpath", ".//div[contains(@class, 'structItem-title')]")
    links = []
    for title in titles:
        link = title.find_element("xpath", ".//a[contains(@href, 'thread')]")
        links.append(link.get_attribute("href"))
        # driver.execute_script("arguments[0].click();", link)
        # time.sleep(15)

    # Opens each link and extracts data
    for link in links:
        driver.get(link)
        articles = driver.find_elements("xpath", ".//article[@class='message message--post js-post js-inlineModContainer  ']")
        for article in articles:
            try:
                users.append(article.find_element("xpath", ".//span[@class='username ' and @itemprop='name']").text)
            except Exception:
                users.append(None)
            try:
                user_type.append(article.find_element("xpath", ".//h5[@itemprop='jobTitle']").text)
            except Exception:
                user_type.append(None)
            user_msg.append(article.find_element("xpath", ".//div[@class='bbWrapper']").text)
            try:
                user_msg_count.append(article.find_elements("xpath", ".//dl[@class='pairs pairs--justified']//child::dd")[1].text)
            except IndexError:
                user_msg_count.append(None)



        time.sleep(0.5w)
    print(page_num)

data = {"user_name": users, "user_type": user_type, "user_msg": user_msg, "user_msg_count": user_msg_count}
df = pd.DataFrame(data=data)
df.to_excel("output.xlsx")


# print(link.get_attribute("href"))
# time.sleep(2)
# link.click()

# for thread in threads:
#     thread.find_element(By.XPATH, "//a[@href]")
# html = driver.page_source
# soup = BeautifulSoup(html,"html.parser")
# threads = soup.find_all("div", class_="structItemContainer-group")
# soup = BeautifulSoup(threads,"html.parser")


