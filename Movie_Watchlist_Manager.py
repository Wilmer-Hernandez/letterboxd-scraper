import requests
from bs4 import BeautifulSoup
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


# Custom exception for invalid year
class InvalidYearError(Exception):
    pass

class MovieScraper:
    def __init__(self, year):
        '''URL for popular films on Letterboxd'''
        self.url_with_all_films = "https://letterboxd.com/films/popular/"
        self.current_year = int(datetime.datetime.now().year)
        self.input_year = int(year)

        # Check if the input year is valid
        if self.input_year > self.current_year or self.input_year <= 1869:
            raise InvalidYearError(f"No movies are recorded in the year {self.input_year}")
        

        # Set up headless Firefox browser for web scraping
        options = Options()
        options.add_argument('-headless')
        self.driver = webdriver.Firefox(options=options)
        self.session = requests.Session()


    def scrape_movies(self):
        # Construct the URL for the specified year
        url_for_each_year = self.url_with_all_films + f"year/{self.input_year}/"
        self.driver.get(url_for_each_year)
        soup_for_each_year = BeautifulSoup(self.driver.page_source, "html.parser")
        movie_list_for_each_year = soup_for_each_year.select_one("ul.poster-list.-p70.-grid")

        if movie_list_for_each_year is None:
            print(f"No movies found for the year {self.input_year}")
            return 

        movies = movie_list_for_each_year.select("li")

        movie_details = []

        for movie in movies:
            # Extract the movie title
            movie_dict = self.process_movies(movie)
            movie_details.append(movie_dict)

        self.driver.quit()

        return movie_details

    def process_movies(self, movie):
        # Extract the movie title
        title_elem = movie.select_one("span.frame-title")
        title_text = title_elem.text.strip().split(" (")[0]
        title = title_text

        # Extract the movie URL
        movie_url_elem = movie.select_one("a.frame")
        movie_url = movie_url_elem["href"]

        # Visit the individual movie page
        movie_response = self.session.get("https://letterboxd.com" + movie_url)
        movie_soup = BeautifulSoup(movie_response.content, "html.parser")

        # Extract movie rating
        movie_rating_elem = movie_soup.select_one('meta[name="twitter:data2"]')
        movie_rating = movie_rating_elem["content"] if movie_rating_elem else "No rating provided by Letterboxd"
        
    
        # Extract movie synopsis
        movie_synopsis_elem = movie_soup.select_one('div.truncate p')
        movie_synopsis = movie_synopsis_elem.text.strip() if movie_synopsis_elem else "No synopsis provided by Letterboxd"

        # Store the movie details in a dictionary
        movie_dict = {
            "Title": title,
            "Rating": movie_rating,
            "Synopsis": movie_synopsis

        }

        return movie_dict
    
try:
    input_year = int(input("Please enter start year (e.g., 2023): "))
    scraper = MovieScraper(input_year)
    movie_details = scraper.scrape_movies()
    
    # Print the movie details
    for movie in movie_details:
        print("Title:", movie["Title"])
        print("Rating:", movie["Rating"])
        print("Synopsis:", movie["Synopsis"])
        print("---------------")

except InvalidYearError as e:
    print(str(e))

