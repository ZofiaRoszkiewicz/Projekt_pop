from tkinter import *
import tkintermapview
import requests
from urllib.parse import quote

# współrzędne wybranych księgarni
ksiegarnia_coords = {
    "TaniaKsiazka_Białystok": (53.1325, 23.1688),
    "Psychebook_Częstochowa": (50.8145, 19.1226),
    "BookBook_Gdańsk": (54.3520, 18.6466),
    "Bonito_Katowice": (50.2610, 19.0235),
    "BIKSA_Katowice": (50.2600, 19.0200),
    "Księgarnia_Akademicka_Katowice": (50.2649, 19.0238),
    "Massolit_Kraków": (50.0628, 19.9395),
    "Lokator_Kraków": (50.0495, 19.9494),
    "DeRevolutionibus_Kraków": (50.0620, 19.9370),
    "Bonobo_Kraków": (50.0621, 19.9363),
    "Matras_Kraków": (50.0647, 19.9450),
    "Świat_Książki_Lublin": (51.2465, 22.5684),
    "Aros_Łódź": (51.7730, 19.4560),
    "Bookszpan_Łódź": (51.7675, 19.4666),
    "AntykwariatTroszkiewiczów_Łódź": (51.7728, 19.4540),
    "Księgarnia_PWN_Łódź": (51.7592, 19.4560),
    "Dedalus_Poznań": (52.4064, 16.9252),
    "Bookarest_Poznań": (52.4065, 16.9330),
    "KsiegarniaŚwWojciecha_Poznań": (52.4096, 16.9312),
    "Matras_Poznań": (52.4089, 16.9347),
    "Empik_Poznań": (52.4091, 16.9350),
    "Księgarnia_Naukowa_Rzeszów": (50.0413, 21.9990),
    "Kulturka_Szczecin": (53.4235, 14.5485),
    "Aros_Wrocław": (51.1079, 17.0385),
    "TajneKomplety_Wrocław": (51.1090, 17.0320),
    "AmericanBookshop_Warszawa": (52.2223, 21.0129),
    "Bookoff_Warszawa": (52.2350, 21.0034),
    "CoLiber_Warszawa": (52.2410, 21.0115),
    "Empik_Warszawa": (52.2297, 21.0122),
    "Thebooks_Warszawa": (52.1218, 21.0336),
}


ksiegarnie = []
ksiegarnia_pracownicy = {}
ksiegarnia_klienci = {}

# lokalizacja punktu na mapie
class Ksiegarnia:
    def __init__(self, nazwa):
        self.nazwa = nazwa
        self.latitude, self.longitude = ksiegarnia_coords.get(self.nazwa, (52.23, 21.0))
        self.marker = map_widget.set_marker(
            self.latitude,
            self.longitude,
            text=self.nazwa.replace("_", " ")
        )

# przypisuje osobę do miasta i księgarni
class Osoba:
    def __init__(self, imie_nazwisko, miasto, nazwa_ksiegarni):
        self.imie_nazwisko = imie_nazwisko
        self.miasto = miasto
        self.nazwa_ksiegarni = nazwa_ksiegarni
        self.latitude, self.longitude = self.get_coordinates()
        self.marker = None

    def get_coordinates(self):
        try:
            url = f"https://nominatim.openstreetmap.org/search.php?q={quote(self.miasto)}&format=jsonv2"
            headers = {"User-Agent": "Mozilla/5.0"}
            resp = requests.get(url, headers=headers)
            data = resp.json()
            return float(data[0]["lat"]), float(data[0]["lon"])
        except Exception as e:
            print(f"Błąd pobierania współrzędnych dla miasta {self.miasto}: {e}")
            return 52.23, 21.0

class Pracownik(Osoba): pass
class Klient(Osoba): pass

def pokaz_ksiegarnie():
    listbox_ksiegarnie.delete(0, END)
    for i, k in enumerate(ksiegarnie):
        listbox_ksiegarnie.insert(i, f"{i+1}. {k.nazwa.replace('_', ' ')}")

def pokaz_na_mapie():
    idx = listbox_ksiegarnie.curselection()
    if not idx:
        return
    ksiegarnia = ksiegarnie[idx[0]]
    map_widget.set_position(ksiegarnia.latitude, ksiegarnia.longitude)
    map_widget.set_zoom(13)

def pokaz_wszystkie_ksiegarnie_na_mapie():
    for k in ksiegarnie:
        if k.marker:
            k.marker.delete()
        k.marker = map_widget.set_marker(k.latitude, k.longitude, text=k.nazwa.replace("_", " "))
    if ksiegarnie:
        lat = sum(k.latitude for k in ksiegarnie) / len(ksiegarnie)
        lon = sum(k.longitude for k in ksiegarnie) / len(ksiegarnie)
        map_widget.set_position(lat, lon)
        map_widget.set_zoom(6)

def pokaz_osoby_dla_ksiegarni(typ):
    idx = listbox_ksiegarnie.curselection()
    if not idx:
        return
    ksiegarnia = ksiegarnie[idx[0]]
    nazwa = ksiegarnia.nazwa
    dane = ksiegarnia_pracownicy if typ == "pracownik" else ksiegarnia_klienci
    osoby = dane.get(nazwa, [])
    for o in osoby:
        if o.marker:
            o.marker.delete()
        o.marker = map_widget.set_marker(
            o.latitude,
            o.longitude,
            text=f"{o.imie_nazwisko}\n({o.miasto})"
        )
    if osoby:
        lat = sum(o.latitude for o in osoby) / len(osoby)
        lon = sum(o.longitude for o in osoby) / len(osoby)
        map_widget.set_position(lat, lon)
        map_widget.set_zoom(7)

def pokaz_wszystkich_pracownikow():
    wszystkie = sum(ksiegarnia_pracownicy.values(), [])
    for o in wszystkie:
        if o.marker:
            o.marker.delete()
        o.marker = map_widget.set_marker(
            o.latitude,
            o.longitude,
            text=f"{o.imie_nazwisko}\n({o.miasto})"
        )
    if wszystkie:
        lat = sum(o.latitude for o in wszystkie) / len(wszystkie)
        lon = sum(o.longitude for o in wszystkie) / len(wszystkie)
        map_widget.set_position(lat, lon)
        map_widget.set_zoom(6)

def pokaz_wszystkich_klientow():
    wszystkie = sum(ksiegarnia_klienci.values(), [])
    for o in wszystkie:
        if o.marker:
            o.marker.delete()
        o.marker = map_widget.set_marker(
            o.latitude,
            o.longitude,
            text=f"{o.imie_nazwisko}\n({o.miasto})"
        )
    if wszystkie:
        lat = sum(o.latitude for o in wszystkie) / len(wszystkie)
        lon = sum(o.longitude for o in wszystkie) / len(wszystkie)
        map_widget.set_position(lat, lon)
        map_widget.set_zoom(6)