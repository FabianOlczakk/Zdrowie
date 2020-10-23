from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from bs4 import BeautifulSoup
from functools import partial
from kivymd.utils import asynckivy
from main import Zdrowie
from asyncfitimage import AsyncImage as AsyncFitImageWidget
from kivymd.uix.list import TwoLineIconListItem
from kivymd.uix.button import ButtonBehavior
from kivy.uix.screenmanager import Screen
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty
from kivymd.uix.list import OneLineIconListItem


class AsyncFitImage(AsyncFitImageWidget):
    pass


class ClickToArticle(TwoLineIconListItem, ButtonBehavior):
    pass


# Tutaj bedzie sie dzial caly web-scraping
class Aktualnosci(BoxLayout):
    # W tej liscie beda przechowywane wszystkie rzeczy z webscrapera, z niej bede pobieral je do apki
    website_content = []
    reversed_website_content = []

    def __init__(self, **kwargs):
        super(Aktualnosci, self).__init__(**kwargs)
        self.app = Zdrowie()
        self.result = ""
        self.src = ""
        self.loaded = False

    def load(self):
        async def load():
            try:
                self.result = UrlRequest("https://wiadomosci.gazeta.pl/wiadomosci/0,173952.html",
                                         on_success=partial(self.update))

                self.loaded = True

            except Exception as e:
                print(e)
                self.screen_manager.current = "no_connection"
                self.loaded = False

        asynckivy.start(load())

    def update(self, *args):
        async def update():
            # print("yeah")
            self.src = self.result.result

            self.website_content.clear()

            soup = BeautifulSoup(self.src, 'lxml')

            # print(soup)

            news_container = soup.find("div", attrs={"class": "main_content"})

            # print(news_container)

            news_list = news_container.findAll("li")

            news_list = news_list[0:5]

            for article in news_list:
                print(article)

        asynckivy.start(update())

    def internet_callback(self):
        pass

    def clear_cards(self):
        async def clear_cards():
            for child in self.children:
                child.header_text.text = ""
                child.sub_text.text = ""
                child.link.link_to_post = ""

        asynckivy.start(clear_cards())

    def refresh_callback(self, *args):
        # Ta funkcja jest wywoływana po odświeżeniu aktualonści
        # Najpier usuwam wszystkie widgety
        def callback(interval):
            self.clear_cards()
            # Ponownie wywkonuje funkcję update()
            self.load()
            self.root.ids.scroll_view_aktualnosci.refresh_done()
            self.app.tick = 0
            print("Odświeżono aktualności")

        Clock.schedule_once(callback, 1)


class OneLineFilterList(OneLineIconListItem):
    """Klasa rzędu z listy krajów"""
    icon = StringProperty()


class CountryFilter(Screen):
    app = Zdrowie()

    default_countries_list = [["Polska", "Poland"], ["Włochy", "Italy"], ["Węgry", "Hungary"], ["Szwecja", "Sweden"],
                              ["Słowenia", "Slovenia"], ["Słowacja", "Slovakia"], ["Rumunia", "Romania"],
                              ["Portugalia", "Portugal"], ["Niemcy", "Germany"], ["Malta", "Malta"],
                              ["Luksemburg", "Luxemburg"], ["Litwa", "Latvia"], ["Irlandia", "Irland"],
                              ["Holandia", "Netherlands"], ["Hiszpania", "Spain"], ["Grecja", "Greece"],
                              ["Francja", "France"], ["Finlandia", "Finland"], ["Estonia", "Estonia"],
                              ["Austria", "Austria"], ["Belgia", "Belgium"], ["Bułgaria", "Bulgaria"],
                              ["Chorwacja", "Croatia"], ["Cypr", "Cyprus"], ["Czechy", "Czech Republic"],
                              ["Dania", "Denmark"]]

    def set_country_filter(self, text="", search=False):
        """Klasa filtrująca kraje"""

        self.recycle_view.data = []

        for country_name in self.default_countries_list:
            print(country_name)
            if self.language == "pl":
                country = country_name[0]
            else:
                country = country_name[1]

            capital_text = text.capitalize()
            if search:
                if capital_text in country:
                    self.recycle_view.data.append({"viewclass": "OneLineFilterList",
                                                   "icon": "earth",
                                                   "text": country,
                                                   })

            else:
                self.recycle_view.data.append({"viewclass": "OneLineFilterList",
                                               "icon": "earth",
                                               "text": country,
                                               })

    def set_default_country(self, country_name):
        """Funkcja ustawiająca koordynaty na wybrane państwo"""
        print(country_name)

        country_list = self.default_countries_list

        country_lat = None
        country_lon = None

        for country in country_list:
            if country_name in country:

                for country_item in self.map.updated_data_list:
                    if country_item[0] == country[1]:
                        print("Ustawianie domyślnego państwa:", country_item)

                        country_lon = country_item[2]
                        country_lat = country_item[3]
                        country_name_pl = country_item[5]
                        country_name_en = country_item[0]

                        self.default_country = [country_name_en, country_name_pl, country_lat, country_lon]

                    else:
                        pass

                self.ustawienia.back_to_home_screen()

            else:
                pass


