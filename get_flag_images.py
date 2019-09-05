import os
from bs4 import BeautifulSoup as Bs
import requests
import os
from multiprocessing.dummy import Pool as ThPool
from datetime import datetime
import sys

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

path = ""
path_split = sys.argv[0].split('\\')[:-1]
for f in path_split:
    path = path + '\\' + f
path = path[1:]+"\images\\"


def save_image(img):

    #path = "C:\Python34\homeworks\images\\"
    url_templ = "http://actravel.ru/images/"
    
    if not os.path.isdir(path):
        os.mkdir(path)
    img_file = requests.get(url_templ + img)
    with open(path+img, "wb") as f:
        f.write(img_file.content)
    #return img_file


if __name__ == '__main__':

    start = datetime.now()
    thnum = len(get_flags_from_site())
    pool = ThPool(thnum)
    results = pool.map(save_image, get_flags_from_site())
    print(len(results))
    pool.close()
    pool.join()
    finish = datetime.now()
    print(finish - start)

