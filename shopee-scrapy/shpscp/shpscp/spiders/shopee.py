import scrapy
import json
from ..items import ShpscpItem
from scrapy.loader import ItemLoader

class ShopeeSpider(scrapy.Spider):
    name = 'shopee'
    allowed_domains = ['shopee.co.id']

    def start_requests(self):
        # cats = {
        #     'Olahraga & Outdoor' : 11043958,
        #     'Perawatan & Kecantikan' : 11043145,
        #     'Pakaian Pria' : 11042849
        # }
        # for cat in cats:
        if self.category == "Olahraga & Outdoor":
            cat = 11043958
        elif self.category == "Perawatan & Kecantikan":
            cat = 11043145
        elif self.category == "Pakaian Pria":
            cat = 11042849

        for newest in range(0, 10000, 60):
            yield scrapy.Request(f'https://shopee.co.id/api/v4/search/search_items?by=relevancy&limit=60&match_id={cat}&newest={newest}&order=desc&page_type=search&scenario=PAGE_OTHERS&version=2', self.parse)

    def parse(self, response):
        items = json.loads(response.body)['items']
        # categori_id = response.url.split("=")[3].split("&")[0]

        for item in items:
            il = ItemLoader(item=ShpscpItem())
            il.add_value('id', item['item_basic']['itemid'])
            il.add_value('name', item['item_basic']['name'])
            il.add_value('price', item['item_basic']['price'])
            il.add_value('categori', self.category)
            il.add_value('sold', item['item_basic']['historical_sold'])
            il.add_value('rate', item['item_basic']['item_rating']['rating_star'])
            il.add_value('place', item['item_basic']['shop_location'])
            yield il.load_item()
    

        