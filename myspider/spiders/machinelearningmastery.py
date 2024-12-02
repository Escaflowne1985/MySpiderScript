import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium.webdriver.common.by import By

num = 1


class SpiderItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    content = scrapy.Field()


class MachinelearningmasterySpider(scrapy.Spider):
    name = "machinelearningmastery"
    # scrapy crawl machinelearningmastery

    allowed_domains = []
    # start_urls = ["https://machinelearningmastery.com/blog/page/1/"]

    start_urls = [
        {
            "category_name":"Attention",
            "category_link":"https://machinelearningmastery.com/category/attention/"
        },
        {
            "category_name":"Better Deep Learning",
            "category_link":"https://machinelearningmastery.com/category/better-deep-learning/"
        },
        {
            "category_name":"Calculus",
            "category_link":"https://machinelearningmastery.com/category/calculus/"
        },
        {
            "category_name":"ChatGPT",
            "category_link":"https://machinelearningmastery.com/category/chatgpt/"
        },
        {
            "category_name":"Code Algorithms",
            "category_link":"https://machinelearningmastery.com/category/algorithms-from-scratch/"
        },
        {
            "category_name":"Computer Vision",
            "category_link":"https://machinelearningmastery.com/category/deep-learning-for-computer-vision/"
        },
        {
            "category_name":"Data Preparation",
            "category_link":"https://machinelearningmastery.com/category/data-preparation/"
        },
        {
            "category_name":"Deep Learning (keras)",
            "category_link":"https://machinelearningmastery.com/category/deep-learning/"
        },
        {
            "category_name":"Deep Learning with PyTorch",
            "category_link":"https://machinelearningmastery.com/category/deep-learning-with-pytorch/"
        },
        {
            "category_name":"Ensemble Learning",
            "category_link":"https://machinelearningmastery.com/category/ensemble-learning/"
        },
        {
            "category_name":"Foundations of Data Science",
            "category_link":"https://machinelearningmastery.com/category/foundations-of-data-science/"
        },
        {
            "category_name":"GANs",
            "category_link":"https://machinelearningmastery.com/category/generative-adversarial-networks/"
        },
        {
            "category_name":"Neural Net Time Series",
            "category_link":"https://machinelearningmastery.com/category/deep-learning-time-series/"
        },
        {
            "category_name":"NLP (Text)",
            "category_link":"https://machinelearningmastery.com/category/natural-language-processing/"
        },
        {
            "category_name":"Imbalanced Learning",
            "category_link":"https://machinelearningmastery.com/category/imbalanced-classification/"
        },
        {
            "category_name":"Intermediate Data Science",
            "category_link":"https://machinelearningmastery.com/category/intermediate-data-science/"
        },
        {
            "category_name":"Intro to Time Series",
            "category_link":"https://machinelearningmastery.com/category/time-series/"
        },
        {
            "category_name":"Intro to Algorithms",
            "category_link":"https://machinelearningmastery.com/category/machine-learning-algorithms/"
        },
        {
            "category_name":"Linear Algebra",
            "category_link":"https://machinelearningmastery.com/category/linear-algebra/"
        },
        {
            "category_name":"LSTMs",
            "category_link":"https://machinelearningmastery.com/category/lstm/"
        },
        {
            "category_name":"OpenCV",
            "category_link":"https://machinelearningmastery.com/category/opencv/"
        },
        {
            "category_name":"Optimization",
            "category_link":"https://machinelearningmastery.com/category/optimization/"
        },
        {
            "category_name":"Probability",
            "category_link":"https://machinelearningmastery.com/category/probability/"
        },
        {
            "category_name":"Python (scikit-learn)",
            "category_link":"https://machinelearningmastery.com/category/python-machine-learning/"
        },
        {
            "category_name":"Python for Machine Learning",
            "category_link":"https://machinelearningmastery.com/category/python-for-machine-learning/"
        }
    ]

    def start_requests(self):
        for url_dict in self.start_urls:
            category = url_dict['category_name']
            url = url_dict['category_link']

            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                meta={'category':category}
            )

    def parse(self, response):
        category = response.meta.get("category", "")  # 确保 category 存在
        # 使用Selenium driver获取动态内容
        driver = response.meta['driver']
        # 显式地重新加载当前URL，确保内容是最新的
        driver.get(response.url)
        # print(response.url)
        html = driver.page_source
        sel = Selector(text=html)

        # 提取文章标题和链接列表
        Item_titles = sel.xpath('//h2[@class="title entry-title"]/a/text()').extract()
        Item_urls = sel.xpath('//h2[@class="title entry-title"]/a/@href').extract()
        print('Item_titles', Item_titles)
        print('Item_urls', Item_urls)

        # 遍历当前页面的所有文章
        for title, url in zip(Item_titles, Item_urls):
            item = SpiderItem()
            item['title'] = title.strip()
            item['url'] = url.strip()
            item["category"] = category
            # print(item)

            # 发起请求到详情页，携带item数据
            yield SeleniumRequest(
                url=item['url'],
                callback=self.parse_detail,
                meta={'item':item}
            )

        # 使用 'sel' 提取下一页链接
        # next_page = sel.xpath("//div[@class='pagination woo-pagination']/div[@class='next page-numbers']/a/@href").get()
        next_page = response.css('a.next.page-numbers::attr(href)').get()
        print("next_page", next_page)
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield SeleniumRequest(
                url=next_page_url,
                callback=self.parse,
                meta={'category':category}
            )

    def parse_detail(self, response):
        # 获取传递过来的item
        item = response.meta['item']

        # 使用Selenium driver获取动态内容
        driver = response.meta['driver']
        html = driver.page_source
        sel = Selector(text=html)

        # 提取详情页的更多信息，例如内容
        item['content'] = sel.css('section.entry').get()
        # print(item['content'])

        # 返回完整的item
        yield item
