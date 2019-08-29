import requests
import certifi
import json
from bs4 import BeautifulSoup
from urllib import parse
from find_in_html import *
import sqlite3
from split_str_to_arr import *
from datetime import datetime
import threading
from multiprocessing.dummy import Pool as ThPool


class Order():

    def __init__(self):
        self.articles = []
        self.exceptions = []

    def process_request(self, item):
        try:
            url = "https://e-dostavka.by/catalog/item_{0}.html".format(item)
            result = requests.get(url).text
            if "К сожалению, по данному запросу товар не найден" not in str(result) and '<div itemprop="offers"' in str(result):
                self.articles.append(item)
                print("{0}\n".format(item))
        except:
            self.exceptions.append(item)
            print('exception {0}'.format(item))



if __name__ == '__main__':

    prod=Order()
    

    pool = ThPool(100)

    start = datetime.now()
    results = pool.map(prod.process_request, range(200000,300000))

    print("pool")
    print(len(results))
    finish = datetime.now()
    pool.close()
    pool.join()
    print(len(prod.articles))    
    print(prod.articles)
    print(len(prod.exceptions))     
    print(prod.exceptions) 
    print(finish - start)


    exc = Order()
    

    pool = ThPool(len(prod.exceptions))

    start = datetime.now()
    results = pool.map(exc.process_request, prod.exceptions)

    print("exceptions")    
    print(len(results))
    finish = datetime.now()
    pool.close()
    pool.join()
    print(len(exc.articles))    
    print(exc.articles)
    print(len(exc.exceptions))     
    print(exc.exceptions) 
    print(finish - start)

    
