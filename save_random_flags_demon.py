import os
from bs4 import BeautifulSoup as Bs
import requests
import os
from multiprocessing.dummy import Pool as ThPool
from datetime import datetime
import sys
from random import random , sample, randint
import time


def get_random_flags(sample_len): #makes sample of .gif file names
    flags = []
    result = requests.get("http://actravel.ru/country_codes.html").text
    html = Bs(result, features="html.parser")
    table = html.find_all("table")[0]
    lines = table.find_all("tr")[1:]
    results_sample = sample(lines, sample_len)     
    for line in results_sample:
        rows = line.find_all("td")
        image = rows[0].find("img").attrs["src"][8:]
        flags.append(image)
    print(flags)
    return flags

path = ""
path_split = sys.argv[0].split('\\')[:-1]
for f in path_split:
    path = path + '\\' + f
path = path[1:]+"\images\\"


def save_image(img): #saves one .gif file

    url_templ = "http://actravel.ru/images/"
    
    if not os.path.isdir(path):
        os.mkdir(path)
    img_file = requests.get(url_templ + img)
    with open(path+img, "wb") as f:
        f.write(img_file.content)

work = True

def demon():
    def worker():
        try:
            while work:
                sample_len = randint(10, 20)
                print("I'll save {0} random flag images, here are their names:".format(sample_len))
                start = datetime.now()
                pool = ThPool(sample_len)
                results = pool.map(save_image, get_random_flags(sample_len))
                print("{0} images are saved.".format(len(results)))
                pool.close()
                pool.join()
                finish = datetime.now()
                print(finish - start)
                sleep_time = randint(5, 10)
                print("Now I go to sleep for {0}sec., good night!\n".format(sleep_time))
                time.sleep(sleep_time)
                #try:
                 #   time.sleep(sleep_time)
                #except KeyboardInterrupt:
                 #   print("Something strange happend, I'll better go away. Good bye!")
                 #   exit(1)    
        except KeyboardInterrupt as e:
            try:
                action = input("Should I have a rest? (y/n)")
                if action == "y":
                    print("Good bye!")
                    exit(0)
                else:
                    worker()
            except:
                worker()

     worker()            


if __name__ == '__main__':
    
    demon()


