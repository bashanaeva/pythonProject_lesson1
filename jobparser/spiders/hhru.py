import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=1&search_field=name&search_field=company_name&search_field=description&text=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82+%D1%81%D1%82%D0%B0%D0%B6%D0%B5%D1%80',
                  'https://hh.ru/search/vacancy?area=2&search_field=name&search_field=company_name&search_field=description&text=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82+%D1%81%D1%82%D0%B0%D0%B6%D0%B5%D1%80']


    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)



    def vacancy_parse(self, response: HtmlResponse):
        # name = response.xpath("//span[@data-qa='vacancy-serp__vacancy-title']//text()").get()
        name = response.xpath("//h3[@data-qa='vacancy-serp__vacancy-title']//text()").get()
        salary = response.xpath("//span[@data-qa='vacancy-serp__vacancy-compensation']//text()").getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)














