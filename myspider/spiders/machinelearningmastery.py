import scrapy

num = 1


class MachinelearningmasterySpider(scrapy.Spider):
    name = "machinelearningmastery"
    allowed_domains = ["machinelearningmastery.com"]
    # start_urls = ["https://machinelearningmastery.com/blog/page/1/"]

    start_urls = [
        {
            "category_name":"Attention",
            "category_link":f"https://machinelearningmastery.com/category/attention/page/{num}/"
        },
        {
            "category_name":"Better Deep Learning",
            "category_link":f"https://machinelearningmastery.com/category/better-deep-learning/page/{num}/"
        },
        {
            "category_name":"Calculus",
            "category_link":f"https://machinelearningmastery.com/category/calculus/page/{num}/"
        },
        {
            "category_name":"ChatGPT",
            "category_link":f"https://machinelearningmastery.com/category/chatgpt/page/{num}/"
        },
        {
            "category_name":"Code Algorithms",
            "category_link":f"https://machinelearningmastery.com/category/algorithms-from-scratch/page/{num}/"
        },
        {
            "category_name":"Computer Vision",
            "category_link":f"https://machinelearningmastery.com/category/deep-learning-for-computer-vision/page/{num}/"
        },
        {
            "category_name":"Data Preparation",
            "category_link":f"https://machinelearningmastery.com/category/data-preparation/page/{num}/"
        },
        {
            "category_name":"Deep Learning (keras)",
            "category_link":f"https://machinelearningmastery.com/category/deep-learning/page/{num}/"
        },
        {
            "category_name":"Deep Learning with PyTorch",
            "category_link":f"https://machinelearningmastery.com/category/deep-learning-with-pytorch/page/{num}/"
        },
        {
            "category_name":"Ensemble Learning",
            "category_link":f"https://machinelearningmastery.com/category/ensemble-learning/page/{num}/"
        },
        {
            "category_name":"Foundations of Data Science",
            "category_link":f"https://machinelearningmastery.com/category/foundations-of-data-science/page/{num}/"
        },
        {
            "category_name":"GANs",
            "category_link":f"https://machinelearningmastery.com/category/generative-adversarial-networks/page/{num}/"
        },
        {
            "category_name":"Neural Net Time Series",
            "category_link":f"https://machinelearningmastery.com/category/deep-learning-time-series/page/{num}/"
        },
        {
            "category_name":"NLP (Text)",
            "category_link":f"https://machinelearningmastery.com/category/natural-language-processing/page/{num}/"
        },
        {
            "category_name":"Imbalanced Learning",
            "category_link":f"https://machinelearningmastery.com/category/imbalanced-classification/page/{num}/"
        },
        {
            "category_name":"Intermediate Data Science",
            "category_link":f"https://machinelearningmastery.com/category/intermediate-data-science/page/{num}/"
        },
        {
            "category_name":"Intro to Time Series",
            "category_link":f"https://machinelearningmastery.com/category/time-series/page/{num}/"
        },
        {
            "category_name":"Intro to Algorithms",
            "category_link":f"https://machinelearningmastery.com/category/machine-learning-algorithms/page/{num}/"
        },
        {
            "category_name":"Linear Algebra",
            "category_link":f"https://machinelearningmastery.com/category/linear-algebra/page/{num}/"
        },
        {
            "category_name":"LSTMs",
            "category_link":f"https://machinelearningmastery.com/category/lstm/page/{num}/"
        },
        {
            "category_name":"OpenCV",
            "category_link":f"https://machinelearningmastery.com/category/opencv/page/{num}/"
        },
        {
            "category_name":"Optimization",
            "category_link":f"https://machinelearningmastery.com/category/optimization/page/{num}/"
        },
        {
            "category_name":"Probability",
            "category_link":f"https://machinelearningmastery.com/category/probability/page/{num}/"
        },
        {
            "category_name":"Python (scikit-learn)",
            "category_link":f"https://machinelearningmastery.com/category/python-machine-learning/page/{num}/"
        },
        {
            "category_name":"Python for Machine Learning",
            "category_link":"fhttps://machinelearningmastery.com/category/python-for-machine-learning/page/{num}/"
        }
    ]

    def parse(self, response):

        # 提取当前页面的数据
        for item in response.css('div.item'):  # 假设每个条目在 div.item 中
            data = {
                'title':item.css('h2::text').get(),
                'url':item.css('a::attr(href)').get(),
                'content':item.css('p::text').get(),
            }
            yield data

        # 查找下一页的链接
        next_page = response.css('a.next::attr(href)').get()  # 假设下一页链接在 <a class="next"> 中

        # 如果找到下一页，递归抓取
        if next_page:
            yield response.follow(next_page, self.parse)
