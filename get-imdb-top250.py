import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver

driver = webdriver.Firefox()

url = 'http://www.imdb.com/chart/top'
driver.get(url)

SCROLL_PAUSE_TIME = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load the page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0",
#            "accept-language": "en-US"}
# response = requests.get(url, headers=headers)
# response.raise_for_status()

# soup = BeautifulSoup(response.text, 'html.parser')
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

items = soup.find_all("li", class_="ipc-metadata-list-summary-item")

imdb_top_250 = []

for item in items:
    rank = item.find('h3', class_='ipc-title__text').text.split('.')[0]
    title = item.find('h3', class_='ipc-title__text').text.split('. ', 1)[1]
    year = item.find('span', class_='cli-title-metadata-item').text
    rating = item.find('span', class_='ipc-rating-star').text.strip().replace("\u00a0", " ")

    print(f"Rank: {rank}, Title: {title}, Year: {year}, Rating: {rating}")

    # Append the details to the list
    imdb_top_250.append({
        'rank': int(rank),
        'title': title,
        'year': int(year),
        'rating': rating,
        'list': "IMDB top 250"
    })

import json

# Store the data in a JSON file
with open('imdb_top250.json', 'w') as f:
    json.dump(imdb_top_250, f, indent=4)