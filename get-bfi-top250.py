import requests
from bs4 import BeautifulSoup
import re
import json

url = "https://www.bfi.org.uk/sight-and-sound/greatest-films-all-time"  # replace with the actual URL

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
# print(soup)

movies = []

# for movie in soup.find_all("a", href=True):
for movie in soup.find_all("article"):
    title = movie.find("h1").text.strip()
    year_country_elements = movie.find("p", class_="ResultsPage__P-sc-of10co-2 eAGqUw")
    year_country = [element.text.strip() for element in year_country_elements]
    year_country = list(filter(None, year_country))
    

    if len(year_country) ==2:
        if re.search(r"\d{4}", year_country[0]):
            year = year_country[0]
            country = year_country[1]
    elif len(year_country) == 1:
        if re.search(r"\d{4}", year_country[0]):
            year = year_country[0]
            country = "Nothing"
    else:
        year = "0"
        country = year_country[0]
    
    # else:
    #     year = country = year_country[0] if year_country else ""

    rank = movie.find("p", class_="ResultsPage__Rank-sc-of10co-1 gHkVaJ PreviewCard__label").text.strip().replace("=", "")
    director = movie.find("p", class_="ResultsPage__P-sc-of10co-2 eAGqUw").find_next("p").text.strip().replace("Directed by ", "")

    print(f"Rank: {rank}, Title: {title}, Year: {year}, Country: {country}, Director: {director}")

    movies.append({
        "rank": int(rank),
        "title": title,
        "year": int(year),
        "country": country,
        "director": director,
        'list': "BFI top 250"
    })

# Store the data in a JSON file
with open('bfi_top250.json', 'w') as f:
    json.dump(movies, f, indent=4)