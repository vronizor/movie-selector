import requests
from bs4 import BeautifulSoup
import json

url = "https://editorial.rottentomatoes.com/guide/best-movies-of-all-time/"  # replace with the actual URL

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

movies = []

for row in soup.find_all("tr"):
    cols = row.find_all("td")
    if len(cols) > 1:
        rank = cols[0].text.strip().replace(".", "")
        movie_element = cols[1].find("span", class_="details")
        title = movie_element.find("a", class_="title").text.strip()
        year = movie_element.find("span", class_="year").text.strip().replace("(", "").replace(")", "")
        rating_element = cols[1].find("span", class_="score-wrap")
        rating = rating_element.find("span", class_="score").text.strip()

        movies.append({
            "rank": int(rank),
            "title": title,
            "year": int(year),
            "rating": rating,
            "list": "Rotten Tomatoes top 300"
        })

# print(movies)
# Store the data in a JSON file
with open('rotten_top300.json', 'w') as f:
    json.dump(movies, f, indent=4)