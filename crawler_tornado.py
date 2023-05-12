import tornado.ioloop
import tornado.web
from tornado.httpclient import AsyncHTTPClient
from bs4 import BeautifulSoup

class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        url = 'https://www.imdb.com/chart/top/'
        http_client = AsyncHTTPClient()

        response = await http_client.fetch(url)
        html_content = response.body

        soup = BeautifulSoup(html_content, 'html.parser')

        movies = []

        for movie_row in soup.select('.lister-list tr'):
            title = movie_row.select_one('.titleColumn a').text
            year = movie_row.select_one('.titleColumn span.secondaryInfo').text.strip('()')
            rating = movie_row.select_one('.ratingColumn strong').text

            movies.append({'title': title, 'year': year, 'rating': rating})

        self.write({'movies': movies})

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
