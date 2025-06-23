
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

def dodaj_ksiegarnie_z_listy():
    nazwa = entry_nazwa.get().strip()
    if not nazwa or nazwa not in ksiegarnia_coords:
        return
    k = Ksiegarnia(nazwa)
    ksiegarnie.append(k)
    ksiegarnia_pracownicy[nazwa] = []
    ksiegarnia_klienci[nazwa] = []
    pokaz_ksiegarnie()
    entry_nazwa.delete(0, END)

def usun_ksiegarnie():
    idx = listbox_ksiegarnie.curselection()
    if not idx:
        return
    i = idx[0]
    ks = ksiegarnie[i]
    for p in ksiegarnia_pracownicy.get(ks.nazwa, []):
        if p.marker:
            p.marker.delete()
    for k in ksiegarnia_klienci.get(ks.nazwa, []):
        if k.marker:
            k.marker.delete()
    if ks.marker:
        ks.marker.delete()
    ksiegarnie.pop(i)
    ksiegarnia_pracownicy.pop(ks.nazwa, None)
    ksiegarnia_klienci.pop(ks.nazwa, None)
    pokaz_ksiegarnie()

def edytuj_ksiegarnie():
    idx = listbox_ksiegarnie.curselection()
    if not idx:
        return
    i = idx[0]
    entry_nazwa.delete(0, END)
    entry_nazwa.insert(0, ksiegarnie[i].nazwa)
    button_dodaj.config(text="Zapisz", command=lambda: zapisz_edycje(i))

def zapisz_edycje(i):
    nowa_nazwa = entry_nazwa.get().strip()
    if not nowa_nazwa:
        return
    if ksiegarnie[i].marker:
        ksiegarnie[i].marker.delete()
    stara = ksiegarnie[i].nazwa
    ksiegarnie[i] = Ksiegarnia(nowa_nazwa)
    ksiegarnia_pracownicy[nowa_nazwa] = ksiegarnia_pracownicy.pop(stara, [])
    ksiegarnia_klienci[nowa_nazwa] = ksiegarnia_klienci.pop(stara, [])
    pokaz_ksiegarnie()
    entry_nazwa.delete(0, END)
    button_dodaj.config(text="Dodaj księgarnię", command=dodaj_ksiegarnie_z_listy)

def otworz_panel_osob(nazwa_typu, typ_klasy, baza_danych):
    idx = listbox_ksiegarnie.curselection()
    if not idx:
        return
    ks = ksiegarnie[idx[0]]
    nazwa_ksiegarni = ks.nazwa
    if nazwa_ksiegarni not in baza_danych:
        baza_danych[nazwa_ksiegarni] = []

    okno = Toplevel(root)
    okno.title(f"{nazwa_typu.capitalize()} – {nazwa_ksiegarni.replace('_', ' ')}")
    okno.geometry("400x550")

    listbox = Listbox(okno, width=50, height=15)
    listbox.pack()

    def odswiez():
        listbox.delete(0, END)
        for i, o in enumerate(baza_danych[nazwa_ksiegarni]):
            listbox.insert(i, f"{i+1}. {o.imie_nazwisko} – {o.miasto}")

    def dodaj():
        imie = entry_imie.get().strip()
        miasto = entry_miasto.get().strip()
        if not imie or not miasto:
            return
        osoba = typ_klasy(imie, miasto, nazwa_ksiegarni)
        baza_danych[nazwa_ksiegarni].append(osoba)
        odswiez()
        entry_imie.delete(0, END)
        entry_miasto.delete(0, END)

    def usun():
        sel = listbox.curselection()
        if not sel:
            return
        o = baza_danych[nazwa_ksiegarni][sel[0]]
        if o.marker:
            o.marker.delete()
        baza_danych[nazwa_ksiegarni].pop(sel[0])
        odswiez()

    def edytuj():
        sel = listbox.curselection()
        if not sel:
            return
        o = baza_danych[nazwa_ksiegarni][sel[0]]
        entry_imie.delete(0, END)
        entry_imie.insert(0, o.imie_nazwisko)
        entry_miasto.delete(0, END)
        entry_miasto.insert(0, o.miasto)
        button_dodaj.config(text="Zapisz", command=lambda: zapisz(sel[0]))

    def zapisz(i_o):
        imie = entry_imie.get().strip()
        miasto = entry_miasto.get().strip()
        if not imie or not miasto:
            return
        o = baza_danych[nazwa_ksiegarni][i_o]
        if o.marker:
            o.marker.delete()
        baza_danych[nazwa_ksiegarni][i_o] = typ_klasy(imie, miasto, nazwa_ksiegarni)
        odswiez()
        entry_imie.delete(0, END)
        entry_miasto.delete(0, END)
        button_dodaj.config(text=f"Dodaj {nazwa_typu.lower()}", command=dodaj)

    Label(okno, text="Imię i nazwisko:").pack()
    entry_imie = Entry(okno, width=40)
    entry_imie.pack()

    Label(okno, text="Miasto:").pack()
    entry_miasto = Entry(okno, width=40)
    entry_miasto.pack()

    button_dodaj = Button(okno, text=f"Dodaj {nazwa_typu.lower()}", command=dodaj)
    button_dodaj.pack(pady=2)
    Button(okno, text=f"Usuń {nazwa_typu.lower()}", command=usun).pack(pady=2)
    Button(okno, text=f"Edytuj {nazwa_typu.lower()}", command=edytuj).pack(pady=2)

    odswiez()

def pokaz_liste_dostepnych_ksiegarni():
    okno = Toplevel(root)
    okno.title("Dostępne księgarnie do dodania")
    okno.geometry("400x400")

    listbox = Listbox(okno, selectmode=MULTIPLE, width=50)
    listbox.pack(pady=10, padx=10, expand=True, fill=BOTH)

    for nazwa in ksiegarnia_coords.keys():
        listbox.insert(END, nazwa)

    def dodaj_zaznaczone():
        wybrane = listbox.curselection()
        for idx in wybrane:
            nazwa = listbox.get(idx)
            if nazwa not in [k.nazwa for k in ksiegarnie]:
                k = Ksiegarnia(nazwa)
                ksiegarnie.append(k)
                ksiegarnia_pracownicy[nazwa] = []
                ksiegarnia_klienci[nazwa] = []
        pokaz_ksiegarnie()
        okno.destroy()

    Button(okno, text="Dodaj zaznaczone", command=dodaj_zaznaczone).pack(pady=10)



root = Tk()
root.title("Projekt systemu do zarządzania siecią księgarni i ich ofertą")
root.geometry("1200x750")

ramka_lista = Frame(root)
ramka_lista.pack(side=LEFT, fill=Y, padx=10, pady=10)

Label(ramka_lista, text="Lista księgarni").pack()
listbox_ksiegarnie = Listbox(ramka_lista, width=40, height=20)
listbox_ksiegarnie.pack()


Button(ramka_lista, text="Wybierz z listy dostępnych księgarni", command=pokaz_liste_dostepnych_ksiegarni).pack(pady=2)
Button(ramka_lista, text="Pokaż na mapie", command=pokaz_na_mapie).pack(pady=2)
Button(ramka_lista, text="Pokaż wszystkie księgarnie", command=pokaz_wszystkie_ksiegarnie_na_mapie).pack(pady=2)
Button(ramka_lista, text="Pracownicy", command=lambda: otworz_panel_osob("pracownik", Pracownik, ksiegarnia_pracownicy)).pack(pady=2)
Button(ramka_lista, text="Klienci", command=lambda: otworz_panel_osob("klient", Klient, ksiegarnia_klienci)).pack(pady=2)
Button(ramka_lista, text="Pokaż wszystkich pracowników", command=pokaz_wszystkich_pracownikow).pack(pady=2)
Button(ramka_lista, text="Pokaż wszystkich klientów", command=pokaz_wszystkich_klientow).pack(pady=2)
Button(ramka_lista, text="Usuń księgarnię", command=usun_ksiegarnie).pack(pady=2)

Label(ramka_lista, text="Edytuj księgarnię").pack(pady=5)
entry_nazwa = Entry(ramka_lista, width=40)
entry_nazwa.pack()
button_dodaj = Button(ramka_lista, text="Zapisz zmiany", command=dodaj_ksiegarnie_z_listy)
button_dodaj.pack(pady=5)



map_widget = tkintermapview.TkinterMapView(root, width=800, height=600, corner_radius=0)
map_widget.pack(side=RIGHT, expand=True, fill=BOTH)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)

root.mainloop()

