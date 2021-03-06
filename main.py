# Moduły kivy
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

# Pozostałe moduł
from toolbar_with_image import MDToolbarWithImage as ToolBarWithImage
import time
import pickle
import os

# Zmienia working directory na folder w którym znajduję się ten plik
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class ContentNavigationDrawer(BoxLayout):
    def update(self):
        self.anchor.clock.update_clock()


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()

    def change_screen(self):
        pass


class ItemDrawerException(OneLineIconListItem):
    icon = StringProperty()

    def change_screen(self):
        pass


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Funkcja wywoływana w momencie kliknięcia na ikone w menu"""

        # Ustawia kolor tekstu i ikony

        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class Zdrowie(MDApp):
    """Główna klasa aplikacji"""

    # Aplikacja dostępna jest w dwóch językach, i tutaj jest zmienna definiująca który język wyświetlać.

    language = StringProperty("pl")
    search_dialog = None
    toolbar_image_source = "images/logo.png"
    color = StringProperty()
    default_country = ListProperty(["Poland"])

    def build(self):
        f = open("config.dat", "rb")

        self.color = pickle.load(f)

        f.close()

        self.theme_cls.primary_palette = self.color
        self.theme_cls.primary_hue = "900"

    def on_start(self):
        self.root.ids.content_drawer.update()
        self.root.ids.corona_map.get_cases_data()
        self.root.ids.aktualnosci.load()

    def set_default_country(self):
        self.default_country = self.root.ids.corona_map.get_default_value()

    def on_color(self, *args):
        print("Color changed to", self.color)

    def change_primary_color(self, color):
        """Funkcja zmienająca i zapsuająca kolor aplikacji"""
        self.theme_cls.primary_palette = color

        f = open("config.dat", "wb")
        pickle.dump(color, f)
        f.close()

    def set_language_to_pl(self):
        self.language = "pl"

    def set_language_to_en(self):
        self.language = "en"
        print(self.language)


class DateTimeClock(BoxLayout):
    date = "sample"
    time = "sample"

    def update_clock(self):
        """Aktualizacja zegaru w menu"""

        def update(interval):
            date_time = time.localtime(time.time())

            if int(date_time[4]) < 10 and int(date_time[5]) < 10:
                self.time = str(date_time[3]) + ":" + "0" + str(date_time[4]) + ":0" + str(date_time[5])

            elif int(date_time[4]) < 10 <= int(date_time[5]):
                self.time = str(date_time[3]) + ":" + "0" + str(date_time[4]) + ":" + str(date_time[5])

            else:
                self.time = str(date_time[3]) + ":" + str(date_time[4]) + ":" + str(date_time[5])

            self.date = str(date_time[2]) + "." + str(date_time[1]) + "." + str(date_time[0])

            for child in self.children:
                child.update()

        Clock.schedule_interval(update, 1)


class DateLabel(MDLabel):
    def update(self, *args):
        self.text = self.clock.date


class TimeLabel(MDLabel):
    def update(self, *args):
        self.text = self.clock.time


class ToolbarWithImage(ToolBarWithImage):
    pass


if __name__ == '__main__':
    Zdrowie().run()
