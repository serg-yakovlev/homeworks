import requests
import certifi
import json
import cities_id
from bs4 import BeautifulSoup
from urllib import parse
import sqlite3


class City():

    def get_city_url(self):
        url='http://dateandtime.info/ru/city.php?id='
        self.city=input("Город (часть названия): ")
        cities = cities_id.cities()
        for c in cities:
            if self.city.lower() in c.lower():
                self.city = c
                city_url = url + cities[c]
                self.city_id=cities[c]
                print(c, city_url)
                return(city_url)
            
    @staticmethod
    def sql_request(city, lat, long):
        sql_r = 'INSERT INTO location ("city", "latitude", "longitude") VALUES ({0}, {1}, {2});'.format('"'+city+'"', lat, long)
        return(sql_r)
            
    def get_wiki_coordinates(self, city):
        ua={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'
        }
        url='https://ru.wikipedia.org/wiki/'+city+'#/maplink/0'
        print(url)
        result=requests.get(url, headers=ua)
        if "В Википедии <b>нет статьи</b> с таким названием" in result.text:
            return("no info")        
        self.html=BeautifulSoup(result.text, features="html.parser") #, 'lxml'
        #print(self.html)
        coord_start=str(self.html).find('"wgCoordinates":{')+len('"wgCoordinates":{')
        rest = str(self.html)[coord_start:]
        coord_end=rest.find('}')
        coordinates=rest[:coord_end]
        #print(coordinates)
        lat = coordinates[6:coordinates.find(',')]
        long = (coordinates[coordinates.find(',')+7:coordinates.find(',')+7+15]).replace('},"','')
        #print('!!!!', lat, 'and!!!!!!!!!!', long)
        return(lat, long)

    @staticmethod
    def grades_to_real(g_m_s):
        try:#         если число градусов  - двузначное
                grades = int(g_m_s[0:2])
                minutes = int(g_m_s[3:5])
                seconds = int(g_m_s[6:8])
        except:
                try:#                        трёхзначное
                    grades = int(g_m_s[0:3])
                    minutes = int(g_m_s[4:6])
                    seconds = int(g_m_s[7:9])
                except:#                     однозначное
                    grades = int(g_m_s[0:1])
                    minutes = int(g_m_s[2:4])
                    seconds = int(g_m_s[5:7])
        return((grades*60*60+minutes*60+seconds)/60/60)
        
    def get_coordinates(self):
        
        ua={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'
        }
        try:
            url=self.get_city_url()
            city = self.city
            #print(url)
            result=requests.get(url, headers=ua)            
            self.html=BeautifulSoup(result.text, features="html.parser") #, 'lxml')
            coordinates=self.html.find_all('div', {'class':'level1'})
            coordinates = str(coordinates[4]).replace('-','')
            self.coordinates=coordinates[coordinates.find("</a>:")+6:coordinates.find("</a>:")+6+30]# строка с координатами
            #разбиваем на 2 строки (широта и долгота) 
            lat = self.coordinates[:8]
            long = self.coordinates[self.coordinates.find(',')+2:self.coordinates.find(',')+2+15]
            #переводим градусы и минуты в десятичную дробь
            self.long = str(self.grades_to_real(long))
            self.lat = str(self.grades_to_real(lat))
        except: # если города нет в списке - идем за координатами в википедию
            coord = self.get_wiki_coordinates(self.city)
            if coord == "no info":
                #print("NO INFO")
                city = input("Ничего не нашлось... Попробуйте указать полное название города: ")
                coord = self.get_wiki_coordinates(city)
            self.lat, self.long = coord
            self.lat = self.lat.replace("\n","")
            self.long = self.long.replace("\n","")
        print('{0}\n{1}'.format(self.lat, self.long))
        sql_r = self.sql_request(city, self.lat, self.long)
        #print(sql_r)

class Weather():

    def __init__(self, lat, long):
        self.url='https://api.weather.yandex.ru/v1/forecast?lat='+lat+'&lon='+long+'&extra=true'

    def send_request(self):
        ua_key={
            'X-Yandex-API-Key': '780b534f-1e57-4e89-8ea0-1fca6d753d7a' #'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
            }
        self.result=requests.get(self.url, headers=ua_key).text
        #self.result='{"now": 1470220206, "now_dt": "2016-08-03T10:30:06.238Z", "info": { "lat": 55.833333, "lon": 37.616667, "tzinfo": { "offset": 10800, "name": "Europe/Moscow", "abbr": "MSK" }, "def_pressure_mm": 746, "def_pressure_pa": 994, "url": "https://yandex.ru/pogoda/moscow" }, "fact": {"temp": 20, "feels_like": 21, "icon": "ovc", "condition": "overcast", "wind_speed": 2, "wind_gust": 5.9, "wind_dir": "n", "pressure_mm": 745, "pressure_pa": 994, "humidity": 83, "daytime": "d", "season": "summer", "prec_type": 1, "prec_strength": 0.25, "cloudness": 1, "obs_time": 1470214800 } }'

    def get_json(self):
        self.json_str=self.result
        
    @staticmethod
    def get_prec(self):
        pass

    @staticmethod
    def get_cloudness(self):
        pass

    @staticmethod
    def get_prec_strength(self):
        pass
    
    @staticmethod
    def get_condition(cond_code):
        try:
            conditions = {
        'clear':'Ясно',
        'partly-cloudy':'Малооблачно',
        'cloudy':'Облачно с прояснениями',
        'overcast':'Пасмурно',
        'partly-cl oudy-and-light-rain':'Небольшой дождь',
        'partly-cloudy-and-rain':'Дождь',
        'overcast-and-rain':'Сильный дождь',
        'overcast-thunderstorms-with-rain': 'Сильный дождь, гроза',
        'cloudy-and-light-rain': 'Небольшой дождь',
        'overcast-and-light-rain':'Небольшой дождь',
        'cloudy-and-rain':'Дождь',
        'overcast-and-wet-snow':'Дождь со снегом',
        'partly-cloudy-and-light-snow':'Небольшой снег',
        'partly-cloudy-and-snow':'Снег',
        'overcast-and-snow':'Снегопад',
        'cloudy-and-light-snow':'Небольшой снег',
        'overcast-and-light-snow':'Небольшой снег',
        'cloudy-and-snow':'Снег',
            }
            return(conditions[cond_code])
        except:
            return("")

    @staticmethod
    def get_wind_direct(wind_direct_code):
         directions = {
        'nw':'северо-западный',
        'n':'северный',
        'ne':'северо-восточный',
        'e':'восточный',
        'se':'юго-восточный',
        's':'южный',
        'sw':'юго-западный',
        'w': 'западный',
        'с': 'штиль'
        }
         return(directions[wind_direct_code])
                
    def json_parce_now(self):
        #780b534f-1e57-4e89-8ea0-1fca6d753d7a
        self.parsed_string = json.loads(self.json_str)
        condition = self.get_condition(self.parsed_string['fact']['condition'])
        temperature = self.parsed_string['fact']['temp']
        temp_perception = self.parsed_string['fact']['feels_like']
        try:
            temp_water = '''\nТемпература воды {0}*C'''.format(self.parsed_string['fact']['temp_water'])
        except:
            temp_water = ''
        wind_direction = str(self.get_wind_direct(self.parsed_string['fact']['wind_dir']))
        wind_speed = self.parsed_string['fact']['wind_speed']
        wind_gust = self.parsed_string['fact']['wind_gust']
        pressure = self.parsed_string['fact']['pressure_mm']
        humidity = str(self.parsed_string['fact']['humidity'])

        weather_now = '''
                Сейчас: \n{0}\nТемпература воздуха {1}*C
Ощущается как {2} *C{3}
Ветер {4}, скорость {5}м/с, порывы до {6} м/с
Атмосферное давление {7} мм. рт. ст.
Относительная влажность {8}%
'''.format(condition, temperature, temp_perception, temp_water, wind_direction, wind_speed, wind_gust, pressure, humidity)
        print(weather_now)
        #return [condition, temperature, temp_perception, temp_water, wind_direction, wind_speed, wind_gust, pressure, humidity]

    #def fill_db(self):
        #condition, temperature, temp_perception, temp_water, wind_direction, wind_speed, wind_gust, pressure, humidity = self.json_parce_now()
        conn = sqlite3.connect("weather_database.db")
        cursor = conn.cursor()
        try:
            cursor.execute("""CREATE TABLE IF NOT EXISTS weather_now
                  (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT , condition text, temperature text, temp_perception text,
                  temp_water text, wind_direction text, wind_speed text, wind_gust text, pressure text, humidity text)
               """)
        except:
            pass

        cursor.execute("""INSERT INTO weather_now (condition, temperature, temp_perception, temp_water, wind_direction, wind_speed, wind_gust,
pressure, humidity) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}' , '{5}' , '{6}' , '{7}' , '{8}' )
                  """.format(condition, temperature, temp_perception, temp_water, wind_direction, wind_speed, wind_gust, pressure, humidity))
        conn.commit()

    def json_parce_fcst(self):
        self.parsed_string = json.loads(self.json_str)
        part=['morning','day','evening','night']
        head=['утро','день','вечер','ночь']
        print('\t\tПрогноз: ')
        for p, h in zip(part, head):
            condition = self.get_condition(self.parsed_string['forecasts'][0]['parts'][p]['condition'])
            temperature = self.parsed_string['forecasts'][0]['parts'][p]['temp_avg']
            temp_perception = self.parsed_string['forecasts'][0]['parts'][p]['feels_like']
            try:
                temp_water = '''\nТемпература воды {0}*C'''.format(self.parsed_string['forecasts'][0]['parts'][p]['temp_water'])
            except:
                temp_water = ''
            wind_direction = str(self.get_wind_direct(self.parsed_string['forecasts'][0]['parts'][p]['wind_dir']))
            wind_speed = self.parsed_string['forecasts'][0]['parts'][p]['wind_speed']
            wind_gust = self.parsed_string['forecasts'][0]['parts'][p]['wind_gust']
            pressure = self.parsed_string['forecasts'][0]['parts'][p]['pressure_mm']
            humidity = str(self.parsed_string['forecasts'][0]['parts'][p]['humidity'])
            weather_fcst = '''
                  {0} \n{1}\nТемпература воздуха {2}*C
Ощущается как {3} *C{4}
Ветер {5}, скорость {6}м/с, порывы до {7} м/с
Атмосферное давление {8} мм. рт. ст.
Относительная влажность {9}%
'''.format(h, condition, temperature, temp_perception, temp_water, wind_direction, wind_speed, wind_gust, pressure, humidity)
            print(weather_fcst)
            #return [p, condition, temperature, temp_perception, temp_water, wind_direction, wind_speed, wind_gust, pressure, humidity]
            conn = sqlite3.connect("weather_database.db")
            cursor = conn.cursor()
            try:
                cursor.execute("""CREATE TABLE IF NOT EXISTS  weather_fcst
                  (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT , part text, condition text, temperature text, temp_perception text,
                  temp_water text, wind_direction text, wind_speed text, wind_gust text, pressure text, humidity text)
               """)
            except:
                pass
        
            cursor.execute("""INSERT INTO weather_fcst (part, condition, temperature, temp_perception, temp_water, wind_direction, wind_speed, wind_gust,
pressure, humidity) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}' , '{5}' , '{6}' , '{7}' , '{8}', '{9}' )
                  """.format(h, condition, temperature, temp_perception, temp_water, wind_direction, wind_speed, wind_gust, pressure, humidity))
            conn.commit()

if __name__ == '__main__':

    c=City()
    c.get_coordinates()
    long=c.long
    lat=c.lat

    w=Weather(lat,long)
    w.send_request()
    w.get_json()
    w.json_parce_now()
    print('\n\n')
    w.json_parce_fcst()
