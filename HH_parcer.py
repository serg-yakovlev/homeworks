import requests
from bs4 import BeautifulSoup
from urllib import parse


class HH():

    def __init__(self):
        self.url=self.__create_url()

    @staticmethod
    def __create_url():
        url="https://hh.ru/"
        return url

    def get_html(self):
        ua={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'
        }
        result=requests.get(self.url, headers=ua)
        #VOZMOZHNA OSHIBKA
        self.html=BeautifulSoup(result.text, features="html.parser") #, 'lxml')

    def find_result(self):
        #self.result_header=self.html.find('h1', {'class':'header header_level-2'}).text
        self.result_vac=self.html.find_all('span', {'class':'vacancy-of-the-day__title'})
        self.result_comp=self.html.find_all('a', {'class':'bloko-link bloko-link_secondary'})
        self.result_link=self.html.find_all('a', {'class':'bloko-link bloko-link_list HH-LinkModifier'})
        self.result_sal=self.html.find_all('span', {'class':'vacancy-of-the-day__salary'})
        
        
    def get_header(self):
        return self.result_header.strip()

    def get_vac(self):
        vac_list = []
        for v, c, s, l in zip(self.result_vac, self.result_comp[1:], self.result_sal, self.result_link):
            #vac_list.append("position: {}, company: {}, salary: {}".format(v.text.ljust(50," "), c.text.ljust(50," "), s.text.ljust(50," ")))
            if len(v.text.strip())>30 and " " in v.text.strip()[30:]:
                print("Position:\t"+v.text.strip()[0:(30+v.text.strip()[30:].find(" "))])
                print("\t\t"+(v.text.strip()[(30+v.text.strip()[30:].find(" ")):]).strip())
            else:
                print("Position:\t"+v.text.strip())
            print("Company:\t"+c.text.strip())
            print("Salary:\t\t"+s.text.strip())
            print("\t\t"+l.get('href')+"\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
            
        #return vac_list
            

    

if __name__=='__main__':
    a=HH()
    a.get_html()
    a.find_result()
    a.get_vac()

