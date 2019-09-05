# import bs4.BeautifulSoup as bs
import os
from bs4 import BeautifulSoup as Bs
import urllib
import requests


#file_name = countries.html
def get_all_country(file_name):
    if os.path.isfile(file_name):
        result = []
        with open(file_name, "r") as html_file:
            html = Bs(html_file.read())
            lines = html.find_all("tr")
            for line in lines:
                rows = line.find_all("td")
                image = rows[0].find("img")
                rus_name = rows[0].text
                bin_code = rows[2].text
                result.append((image.attrs["src"], rus_name, bin_code))
        return result
    else:
        raise ValueError("File '{0}' not found!".format(file_name))

def get_flags(file_name):
    if os.path.isfile(file_name):
        result = []
        with open(file_name, "r") as html_file:
            html = Bs(html_file.read())#, features="html.parser")
            lines = html.find_all("tr")
            for line in lines:
                rows = line.find_all("td")
                image = rows[0].find("img").attrs["src"][8:]
                result.append(image)
        return result
    else:
        raise ValueError("File '{0}' not found!".format(file_name))

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
    print(flags)
    return flags


def save_images():
    url_templ = "http://actravel.ru/images/"
    flags = get_flags_from_site()
    for flag in flags:
        img = requests.get(url_templ + flag)
        with open(flag, "wb") as f:
            f.write(img.content)


def get_sql_country(data):
    pass


if __name__ == '__main__':
    #res = get_flags("countries.html")
    #print(res)
    save_images()
