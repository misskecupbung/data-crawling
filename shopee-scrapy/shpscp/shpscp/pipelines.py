# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector

class ShpscpPipeline:

    def __init__(self):
        self.con = mysql.connector.connect(
            host = '192.168.10.151',
            port = '3306',
            user = 'crawl',
            passwd = 'pmld',
            database = 'dbdatacollector'
        )
        self.cur = self.con.cursor()
        # self.create_table()

    # def create_table(self):
    #     self.cur.execute("""DROP TABLE IF EXISTS item""")
    #     self.cur.execute("""CREATE TABLE item( ItemId REAL PRIMARY KEY, ItemName TEXT, ItemPrice INTEGER, ItemSold INTEGER, ItemCategories TEXT, ItemRate FLOAT(2,1), ItemFrom TEXT)""")


    def process_item(self, item, spider):
        self.cur.execute("""INSERT INTO item VALUES (%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE name=%s, price=%s, sold=%s, place=%s, rate=%s""", (item['id'], item['name'], item['price'], item['sold'], item['place'], item['rate'], item['categori'], item['name'], item['price'], item['sold'], item['place'], item['rate']))
        self.con.commit()
        return item
