from bs4 import BeautifulSoup
import requests

url = "https://www.imdb.com/chart/top"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

movie_list = soup.find("tbody", class_="lister-list")
movies = movie_list.find_all("tr")

for movie in movies:
    rank = movie.find("td", class_="titleColumn").get_text(strip=True)
    title = movie.find("td", class_="titleColumn").a.get_text(strip=True)
    rating = movie.find("td", class_="ratingColumn").strong.get_text(strip=True)
    print(f"Rank: {rank}, Title: {title}, Rating: {rating}")