import requests
from bs4 import BeautifulSoup

url = 'https://www.imdb.com/chart/top/'
response = requests.get(url)
html_content = response.content

soup = BeautifulSoup(html_content, 'html.parser')

movies = []

for movie_row in soup.select('.lister-list tr'):
    title = movie_row.select_one('.titleColumn a').text
    year = movie_row.select_one('.titleColumn span.secondaryInfo').text.strip('()')
    rating = movie_row.select_one('.ratingColumn strong').text

    movies.append({'title': title, 'year': year, 'rating': rating})

for movie in movies:
    print(f"{movie['title']} ({movie['year']}) - Rating: {movie['rating']}")
