import scrapy

num = 1

import scrapy


class SpiderItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()


class MachinelearningmasterySpider(scrapy.Spider):
    name = "machinelearningmastery"
    allowed_domains = ["machinelearningmastery.com"]
    # start_urls = ["https://machinelearningmastery.com/blog/page/1/"]

    start_urls = [
        {
            "category_name": "Attention",
            "category_link": f"https://machinelearningmastery.com/category/attention/page/{num}/"
        },
        {
            "category_name": "Better Deep Learning",
            "category_link": f"https://machinelearningmastery.com/category/better-deep-learning/page/{num}/"
        },
        {
            "category_name": "Calculus",
            "category_link": f"https://machinelearningmastery.com/category/calculus/page/{num}/"
        },
        {
            "category_name": "ChatGPT",
            "category_link": f"https://machinelearningmastery.com/category/chatgpt/page/{num}/"
        },
        {
            "category_name": "Code Algorithms",
            "category_link": f"https://machinelearningmastery.com/category/algorithms-from-scratch/page/{num}/"
        },
        {
            "category_name": "Computer Vision",
            "category_link": f"https://machinelearningmastery.com/category/deep-learning-for-computer-vision/page/{num}/"
        },
        {
            "category_name": "Data Preparation",
            "category_link": f"https://machinelearningmastery.com/category/data-preparation/page/{num}/"
        },
        {
            "category_name": "Deep Learning (keras)",
            "category_link": f"https://machinelearningmastery.com/category/deep-learning/page/{num}/"
        },
        {
            "category_name": "Deep Learning with PyTorch",
            "category_link": f"https://machinelearningmastery.com/category/deep-learning-with-pytorch/page/{num}/"
        },
        {
            "category_name": "Ensemble Learning",
            "category_link": f"https://machinelearningmastery.com/category/ensemble-learning/page/{num}/"
        },
        {
            "category_name": "Foundations of Data Science",
            "category_link": f"https://machinelearningmastery.com/category/foundations-of-data-science/page/{num}/"
        },
        {
            "category_name": "GANs",
            "category_link": f"https://machinelearningmastery.com/category/generative-adversarial-networks/page/{num}/"
        },
        {
            "category_name": "Neural Net Time Series",
            "category_link": f"https://machinelearningmastery.com/category/deep-learning-time-series/page/{num}/"
        },
        {
            "category_name": "NLP (Text)",
            "category_link": f"https://machinelearningmastery.com/category/natural-language-processing/page/{num}/"
        },
        {
            "category_name": "Imbalanced Learning",
            "category_link": f"https://machinelearningmastery.com/category/imbalanced-classification/page/{num}/"
        },
        {
            "category_name": "Intermediate Data Science",
            "category_link": f"https://machinelearningmastery.com/category/intermediate-data-science/page/{num}/"
        },
        {
            "category_name": "Intro to Time Series",
            "category_link": f"https://machinelearningmastery.com/category/time-series/page/{num}/"
        },
        {
            "category_name": "Intro to Algorithms",
            "category_link": f"https://machinelearningmastery.com/category/machine-learning-algorithms/page/{num}/"
        },
        {
            "category_name": "Linear Algebra",
            "category_link": f"https://machinelearningmastery.com/category/linear-algebra/page/{num}/"
        },
        {
            "category_name": "LSTMs",
            "category_link": f"https://machinelearningmastery.com/category/lstm/page/{num}/"
        },
        {
            "category_name": "OpenCV",
            "category_link": f"https://machinelearningmastery.com/category/opencv/page/{num}/"
        },
        {
            "category_name": "Optimization",
            "category_link": f"https://machinelearningmastery.com/category/optimization/page/{num}/"
        },
        {
            "category_name": "Probability",
            "category_link": f"https://machinelearningmastery.com/category/probability/page/{num}/"
        },
        {
            "category_name": "Python (scikit-learn)",
            "category_link": f"https://machinelearningmastery.com/category/python-machine-learning/page/{num}/"
        },
        {
            "category_name": "Python for Machine Learning",
            "category_link": "fhttps://machinelearningmastery.com/category/python-for-machine-learning/page/{num}/"
        }
    ]

    def start_requests(self):
        for url_dict in self.start_urls:
            category = url_dict['category_name']
            url = url_dict['category_link']

            yield scrapy.Request(
                url=url,
                meta={
                    'category': category,
                },
                callback=self.parse
            )

    def parse(self, response):
        # 提取文章标题和链接列表
        Item_titles = response.xpath('//h2[@class="title entry-title"]/a/text()').extract()
        Item_urls = response.xpath('//h2[@class="title entry-title"]/a/@href').extract()

        # 遍历当前页面的所有文章
        for title, url in zip(Item_titles, Item_urls):
            item = SpiderItem()
            item['title'] = title.strip()
            item['url'] = url.strip()
            item["category"] = response.meta.get("category", "")  # 确保 category 存在

            # 发起请求到详情页，携带 item 数据
            yield scrapy.Request(
                item['url'],
                callback=self.parse_detail,
                meta={'item': item}
            )

        # 在处理完所有文章后，查找下一页链接
        next_page = response.css('a.next.page-numbers::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response):
        # 获取传递过来的 item
        item = response.meta['item']

        # 在此处提取详情页的更多信息，示例：
        item['content'] = response.css('div.content').get()

        # 返回完整的 item
        yield item
