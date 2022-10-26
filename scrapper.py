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
options.add_argument("enable-automation")
options.add_argument("--no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--dns-prefetch-disable")
options.add_argument("--disable-gpu")
options.add_argument('--headless')
options.add_argument("--window-size=1920,1080")
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

users = []
user_type = []
user_msg = []
user_msg_count = []
forum_types = []

inital_link = "https://www.mentalhealthforum.net/forum/"

driver.get(inital_link)

driver.get_screenshot_as_file("screen.png")

try:
    forum_block = driver.find_element("xpath", "//div[@class='block block--category block--category401 collapsible-nodes']")
    time.sleep(2)
    forums = forum_block.find_elements("xpath", ".//div[contains(@class,'node node')]")

    print(len(forums))

    forum_links = [forum.find_element("xpath", ".//a[contains(@data-shortcut,'node-description')]").get_attribute("href") for forum in forums]

    for forum_link in forum_links[:2]:

        driver.get(forum_link)
        forum_type = driver.find_element("xpath", ".//h1[@class='p-title-value']").text.replace(" ", "_")
        print(f"Forum: {forum_type}")
        # Returns max page number of forum
        max_page_label = driver.find_elements("xpath", "//li[contains(@class,'pageNav-page')]")[-1]
        forum_max_page = int(max_page_label.find_element("xpath", ".//a[@href]").text)

        max_page_allowed = 3
        if forum_max_page >= max_page_allowed:
            forum_max_page = max_page_allowed

        for page_num in range(1, forum_max_page, 1):
            page_num = f"page-{page_num}"
            driver.get(forum_link + page_num)
            # Returns all links of the page in a list called links
            thread_container = driver.find_element("xpath", "//div[@class='structItemContainer-group js-threadList']")
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
                    try:
                        forum_types.append(forum_type)
                    except Exception:
                        forum_types.append(None)
                time.sleep(0.25)
            print(page_num)
except Exception:
    print("Error encountered. Inserted NULL")
finally:
    data = {"user_name": users, "user_type": user_type, "user_msg": user_msg, "user_msg_count": user_msg_count, "forum_type": forum_types}
    df = pd.DataFrame(data=data)
    df.to_csv("result/mental_health_forum_data.csv")
    print("Job Finished")




# print(link.get_attribute("href"))
# time.sleep(2)
# link.click()

# for thread in threads:
#     thread.find_element(By.XPATH, "//a[@href]")
# html = driver.page_source
# soup = BeautifulSoup(html,"html.parser")
# threads = soup.find_all("div", class_="structItemContainer-group")
# soup = BeautifulSoup(threads,"html.parser")


