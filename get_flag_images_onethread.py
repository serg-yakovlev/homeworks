# import bs4.BeautifulSoup as bs
import os
from bs4 import BeautifulSoup as Bs
import requests
import os
from multiprocessing.dummy import Pool as ThPool
from datetime import datetime

def get_flags_from_site():
    flags = []
    result = requests.get("http://actravel.ru/country_codes.html").text
    html = Bs(result, features="html.parser")
    table = html.find_all("table")[0]
    lines = table.find_all("tr")[1:]
    for line in lines:
        rows = line.find_all("td")
        image = rows[0].find("img").attrs["src"][8:]
        flags.append(image)
    return flags


def save_images():
    path = "C:\Python34\homeworks\images\\"
    url_templ = "http://actravel.ru/images/"
    
    if not os.path.isdir(path):
        os.mkdir(path)
    flags = get_flags_from_site()
    for flag in flags:
        img_file = requests.get(url_templ + flag)
        with open(path+flag, "wb") as f:
            f.write(img_file.content)



if __name__ == '__main__':

    start = datetime.now()    
    save_images()
    finish = datetime.now()
    print(finish - start)
