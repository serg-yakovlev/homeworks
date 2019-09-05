# import bs4.BeautifulSoup as bs
import os
from bs4 import BeautifulSoup as Bs
from urllib3 import request

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
        raise ValueError(f"File '{file_name}' not found!")

def get_flags(file_name):
    if os.path.isfile(file_name):
        result = []
        with open(file_name, "r") as html_file:
            html = Bs(html_file.read(), features="html.parser")
            lines = html.find_all("tr")
            for line in lines:
                rows = line.find_all("td")
                image = rows[0].find("img").attrs["src"][8:]
                result.append(image)
        return result
    else:
        raise ValueError(f"File '{file_name}' not found!")

def save_images():
    url_templ = "http://actravel.ru/images/"
    flags = get_flags("countries.html")
    for flag in flags:
        with open(flag, "w") as f:
            #print(url_templ+flag)
            #url = url_templ+flag
            request.urlretrieve(url_templ+flag, flag)
            #f.write(result)

def get_sql_country(data):
    pass


if __name__ == '__main__':
    #res = get_flags("countries.html")
    #print(res)
    save_images()
