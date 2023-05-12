import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    start_urls = ['https://www.imdb.com/chart/top/']

    def parse(self, response):
        for movie in response.css('.lister-list tr'):
            yield {
                'title': movie.css('.titleColumn a::text').get(),
                'year': movie.css('.titleColumn span.secondaryInfo::text').get().strip('()'),
                'rating': movie.css('.ratingColumn strong::text').get()
            }
